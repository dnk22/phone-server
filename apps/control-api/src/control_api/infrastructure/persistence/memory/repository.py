import asyncio
from datetime import UTC, datetime, timedelta
from uuid import NAMESPACE_URL, UUID, uuid5

from control_api.modules.automation_tasks.models import AutomationTaskRecord
from control_api.modules.device_agents.models import DeviceAgentRecord
from control_api.shared.errors import ForbiddenError, NotFoundError

from contracts import (
    AgentLifecycleStatus,
    AutomationTaskStatus,
    CapabilityReport,
    CapabilityStatus,
    ClaimTaskRequest,
    DeviceReport,
    TaskLogEntry,
)


class MemoryRepository:
    def __init__(self, *, heartbeat_timeout_seconds: int = 60) -> None:
        self._lock = asyncio.Lock()
        self._agents: dict[UUID, DeviceAgentRecord] = {}
        self._agent_external_index: dict[str, UUID] = {}
        self._device_index: dict[UUID, tuple[UUID, str]] = {}
        self._device_external_index: dict[tuple[UUID, str], UUID] = {}
        self._tasks: dict[UUID, AutomationTaskRecord] = {}
        self._heartbeat_timeout_seconds = heartbeat_timeout_seconds

    def effective_agent_status(
        self, agent: DeviceAgentRecord, *, now: datetime | None = None
    ) -> AgentLifecycleStatus:
        if agent.status in {AgentLifecycleStatus.REVOKED, AgentLifecycleStatus.ERROR}:
            return agent.status
        if agent.last_seen_at is None:
            return agent.status
        current = now or datetime.now(UTC)
        if current - agent.last_seen_at > timedelta(seconds=self._heartbeat_timeout_seconds):
            return AgentLifecycleStatus.OFFLINE
        return agent.status

    async def upsert_registration(self, agent: DeviceAgentRecord) -> DeviceAgentRecord:
        async with self._lock:
            existing_id = self._agent_external_index.get(agent.external_id)
            if existing_id is None:
                self._agents[agent.id] = agent
                self._agent_external_index[agent.external_id] = agent.id
                return agent
            existing = self._agents[existing_id]
            if existing.status == AgentLifecycleStatus.REVOKED:
                raise ForbiddenError("revoked agent cannot register")
            existing.name = agent.name
            existing.agent_version = agent.agent_version
            existing.platform = agent.platform
            existing.architecture = agent.architecture
            return existing

    async def get_agent(self, agent_id: UUID) -> DeviceAgentRecord:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise NotFoundError("agent not found") from exc

    async def get_agent_by_external_id(self, external_id: str) -> DeviceAgentRecord:
        agent_id = self._agent_external_index.get(external_id)
        if agent_id is None:
            raise NotFoundError("agent not found")
        return self._agents[agent_id]

    async def list_agents(
        self, status: AgentLifecycleStatus | None = None
    ) -> list[DeviceAgentRecord]:
        agents = list(self._agents.values())
        if status is None:
            return agents
        return [agent for agent in agents if self.effective_agent_status(agent) == status]

    async def update_agent(self, agent: DeviceAgentRecord) -> DeviceAgentRecord:
        async with self._lock:
            self._agents[agent.id] = agent
            return agent

    async def update_agent_reports(
        self,
        agent: DeviceAgentRecord,
        *,
        capabilities: list[CapabilityReport],
        devices: list[DeviceReport],
        seen_at: datetime,
    ) -> None:
        async with self._lock:
            agent.capabilities = capabilities
            agent.devices = devices
            agent.last_seen_at = seen_at
            for report in devices:
                key = (agent.id, report.external_id)
                device_id = self._device_external_index.get(key)
                if device_id is None:
                    device_id = uuid5(NAMESPACE_URL, f"{agent.id}:{report.external_id}")
                    self._device_external_index[key] = device_id
                    self._device_index[device_id] = key

    async def get_device(self, device_id: UUID) -> tuple[DeviceAgentRecord, DeviceReport]:
        pair = self._device_index.get(device_id)
        if pair is None:
            raise NotFoundError("device not found")
        agent = await self.get_agent(pair[0])
        for device in agent.devices:
            if device.external_id == pair[1]:
                return agent, device
        raise NotFoundError("device not found")

    async def list_agent_devices(self, agent_id: UUID) -> list[DeviceReport]:
        agent = await self.get_agent(agent_id)
        return agent.devices

    async def create_task(self, task: AutomationTaskRecord) -> AutomationTaskRecord:
        async with self._lock:
            self._tasks[task.id] = task
            return task

    async def get_task(self, task_id: UUID) -> AutomationTaskRecord:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise NotFoundError("task not found") from exc

    async def list_tasks(self) -> list[AutomationTaskRecord]:
        return list(self._tasks.values())

    async def claim_task(self, request: ClaimTaskRequest) -> AutomationTaskRecord | None:
        async with self._lock:
            agent = await self.get_agent_by_external_id(request.agent_external_id)
            if self.effective_agent_status(agent) != AgentLifecycleStatus.CONNECTED:
                return None
            device_external_ids = set(request.available_device_ids)
            for task in self._tasks.values():
                if task.status != AutomationTaskStatus.QUEUED:
                    continue
                pair = self._device_index.get(task.target_device_id)
                if pair is None or pair[0] != agent.id or pair[1] not in device_external_ids:
                    continue
                device = next((item for item in agent.devices if item.external_id == pair[1]), None)
                if device is None or device.busy:
                    continue
                capability_map = {
                    cap.name: cap.status for cap in device.capabilities + agent.capabilities
                }
                if any(
                    capability_map.get(name) != CapabilityStatus.AVAILABLE
                    for name in task.required_capabilities
                ):
                    continue
                task.status = AutomationTaskStatus.ASSIGNED
                task.agent_id = agent.id
                task.assigned_at = datetime.now(UTC)
                task.updated_at = task.assigned_at
                return task
            return None

    async def add_task_log_entries(self, task_id: UUID, entries: list[TaskLogEntry]) -> int:
        async with self._lock:
            task = await self.get_task(task_id)
            added = 0
            for entry in entries:
                key = str(entry.event_id)
                if key in task.log_event_ids:
                    continue
                task.log_event_ids.add(key)
                task.log_entries.append(entry)
                added += 1
            return added

    async def update_task(self, task: AutomationTaskRecord) -> AutomationTaskRecord:
        async with self._lock:
            if task.id not in self._tasks:
                raise NotFoundError("task not found")
            self._tasks[task.id] = task
            return task
