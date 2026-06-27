import secrets
from datetime import timedelta
from uuid import UUID

from control_api.core.config import ControlApiSettings
from control_api.infrastructure.persistence.memory.repository import MemoryRepository
from control_api.modules.device_agents.models import DeviceAgentRecord
from control_api.shared.errors import ConflictError, ForbiddenError

from contracts import (
    AgentHeartbeatRequest,
    AgentHeartbeatResponse,
    AgentLifecycleStatus,
    AgentRegistrationRequest,
    AgentRegistrationResponse,
    AgentSummary,
    utc_now,
)


class DeviceAgentService:
    def __init__(self, repository: MemoryRepository, settings: ControlApiSettings) -> None:
        self._repository = repository
        self._settings = settings

    async def register(self, request: AgentRegistrationRequest) -> AgentRegistrationResponse:
        record = DeviceAgentRecord(
            external_id=request.agent_external_id,
            name=request.name,
            agent_version=request.agent_version,
            platform=request.platform,
            architecture=request.architecture,
        )
        agent = await self._repository.upsert_registration(record)
        return AgentRegistrationResponse(
            agent_id=agent.id,
            agent_external_id=agent.external_id,
            status=agent.status,
            pairing_code=agent.pairing_code,
            heartbeat_interval_seconds=self._settings.heartbeat_interval_seconds,
            server_time=utc_now(),
        )

    async def heartbeat(self, request: AgentHeartbeatRequest) -> AgentHeartbeatResponse:
        agent = await self._repository.get_agent_by_external_id(request.agent_external_id)
        if agent.status == AgentLifecycleStatus.REVOKED:
            raise ForbiddenError("revoked agent cannot heartbeat")
        await self._repository.update_agent_reports(
            agent,
            capabilities=request.capabilities,
            devices=request.devices,
            seen_at=utc_now(),
        )
        return AgentHeartbeatResponse(
            agent_status=agent.status,
            server_time=utc_now(),
            next_heartbeat_seconds=self._settings.heartbeat_interval_seconds,
            commands=[],
        )

    async def list_agents(self, status: AgentLifecycleStatus | None = None) -> list[AgentSummary]:
        return [self._summary(agent) for agent in await self._repository.list_agents(status)]

    async def get_agent(self, agent_id: UUID) -> AgentSummary:
        return self._summary(await self._repository.get_agent(agent_id))

    async def start_pairing(self, agent_id: UUID) -> AgentSummary:
        agent = await self._repository.get_agent(agent_id)
        if agent.status == AgentLifecycleStatus.REVOKED:
            raise ConflictError("revoked agent cannot be paired")
        agent.status = AgentLifecycleStatus.PENDING_PAIRING
        agent.pairing_code = secrets.token_urlsafe(8)
        agent.pairing_expires_at = utc_now() + timedelta(
            seconds=self._settings.pairing_code_ttl_seconds
        )
        await self._repository.update_agent(agent)
        return self._summary(agent)

    async def approve(self, agent_id: UUID) -> AgentSummary:
        agent = await self._repository.get_agent(agent_id)
        if agent.status != AgentLifecycleStatus.PENDING_PAIRING:
            raise ConflictError("agent is not pending pairing")
        if agent.pairing_expires_at is not None and agent.pairing_expires_at < utc_now():
            raise ConflictError("pairing code expired")
        agent.status = AgentLifecycleStatus.CONNECTED
        agent.paired_at = utc_now()
        agent.token_hash = secrets.token_urlsafe(24)
        await self._repository.update_agent(agent)
        return self._summary(agent)

    async def disconnect(self, agent_id: UUID) -> AgentSummary:
        agent = await self._repository.get_agent(agent_id)
        if agent.status == AgentLifecycleStatus.REVOKED:
            return self._summary(agent)
        agent.status = AgentLifecycleStatus.DISCOVERED
        agent.paired_at = None
        agent.token_hash = None
        await self._repository.update_agent(agent)
        return self._summary(agent)

    async def revoke(self, agent_id: UUID) -> AgentSummary:
        agent = await self._repository.get_agent(agent_id)
        agent.status = AgentLifecycleStatus.REVOKED
        agent.revoked_at = utc_now()
        agent.token_hash = None
        await self._repository.update_agent(agent)
        return self._summary(agent)

    def _summary(self, agent: DeviceAgentRecord) -> AgentSummary:
        return AgentSummary(
            id=agent.id,
            external_id=agent.external_id,
            name=agent.name,
            status=agent.status,
            effective_status=self._repository.effective_agent_status(agent),
            agent_version=agent.agent_version,
            platform=agent.platform,
            architecture=agent.architecture,
            last_seen_at=agent.last_seen_at,
            paired_at=agent.paired_at,
            revoked_at=agent.revoked_at,
        )
