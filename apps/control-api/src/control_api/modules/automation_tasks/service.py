from uuid import UUID

from control_api.infrastructure.persistence.memory.repository import MemoryRepository
from control_api.modules.automation_tasks.models import AutomationTaskRecord
from control_api.modules.automation_tasks.state_machine import validate_transition
from control_api.modules.device_agents.readiness import calculate_readiness
from control_api.shared.errors import ConflictError

from contracts import (
    AutomationTask,
    AutomationTaskAssignment,
    AutomationTaskStatus,
    ClaimTaskRequest,
    CreateAutomationTaskRequest,
    TaskFailureReport,
    TaskLogBatch,
    TaskProgressReport,
    TaskResultReport,
    utc_now,
)


class AutomationTaskService:
    def __init__(self, repository: MemoryRepository) -> None:
        self._repository = repository

    async def create(self, request: CreateAutomationTaskRequest) -> AutomationTask:
        agent, device = await self._repository.get_device(request.target_device_id)
        readiness = calculate_readiness(
            agent,
            device,
            effective_status=self._repository.effective_agent_status(agent),
        )
        if not readiness.ready:
            raise ConflictError(f"device is not automation-ready: {','.join(readiness.reasons)}")
        task = AutomationTaskRecord(
            target_device_id=request.target_device_id,
            scenario_id=request.scenario_id,
            scenario_version=request.scenario_version,
            payload=request.payload,
            required_capabilities=request.required_capabilities,
        )
        return self._to_contract(await self._repository.create_task(task))

    async def list(self) -> list[AutomationTask]:
        return [self._to_contract(task) for task in await self._repository.list_tasks()]

    async def get(self, task_id: UUID) -> AutomationTask:
        return self._to_contract(await self._repository.get_task(task_id))

    async def claim(self, request: ClaimTaskRequest) -> AutomationTaskAssignment | None:
        task = await self._repository.claim_task(request)
        if task is None:
            return None
        return AutomationTaskAssignment(task=self._to_contract(task))

    async def accept(self, task_id: UUID) -> AutomationTask:
        return await self._transition(task_id, AutomationTaskStatus.ACCEPTED)

    async def start(self, task_id: UUID) -> AutomationTask:
        return await self._transition(task_id, AutomationTaskStatus.RUNNING)

    async def cancel(self, task_id: UUID) -> AutomationTask:
        return await self._transition(task_id, AutomationTaskStatus.CANCELLED)

    async def progress(self, task_id: UUID, report: TaskProgressReport) -> AutomationTask:
        task = await self._repository.get_task(task_id)
        if task.status != AutomationTaskStatus.RUNNING:
            raise ConflictError("progress can only be reported for running tasks")
        task.progress = report.progress
        task.updated_at = utc_now()
        return self._to_contract(await self._repository.update_task(task))

    async def logs(self, task_id: UUID, batch: TaskLogBatch) -> dict[str, int]:
        added = await self._repository.add_task_log_entries(task_id, batch.entries)
        return {"accepted": len(batch.entries), "stored": added}

    async def complete(self, task_id: UUID, report: TaskResultReport) -> AutomationTask:
        task = await self._repository.get_task(task_id)
        validate_transition(task.status, AutomationTaskStatus.SUCCEEDED)
        task.status = AutomationTaskStatus.SUCCEEDED
        task.progress = 100
        task.result = report.result
        task.updated_at = utc_now()
        return self._to_contract(await self._repository.update_task(task))

    async def fail(self, task_id: UUID, report: TaskFailureReport) -> AutomationTask:
        task = await self._repository.get_task(task_id)
        validate_transition(task.status, AutomationTaskStatus.FAILED)
        task.status = AutomationTaskStatus.FAILED
        task.error = report.error
        task.result = report.result
        task.updated_at = utc_now()
        return self._to_contract(await self._repository.update_task(task))

    async def _transition(self, task_id: UUID, desired: AutomationTaskStatus) -> AutomationTask:
        task = await self._repository.get_task(task_id)
        validate_transition(task.status, desired)
        task.status = desired
        task.updated_at = utc_now()
        return self._to_contract(await self._repository.update_task(task))

    def _to_contract(self, task: AutomationTaskRecord) -> AutomationTask:
        return AutomationTask(
            id=task.id,
            target_device_id=task.target_device_id,
            agent_id=task.agent_id,
            scenario_id=task.scenario_id,
            scenario_version=task.scenario_version,
            payload=task.payload,
            required_capabilities=task.required_capabilities,
            status=task.status,
            progress=task.progress,
            result=task.result,
            error=task.error,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
