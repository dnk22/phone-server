# ruff: noqa: B008
from uuid import UUID

from control_api.api.dependencies import get_automation_task_service
from control_api.modules.automation_tasks.service import AutomationTaskService
from fastapi import APIRouter, Depends

from contracts import (
    AutomationTask,
    AutomationTaskAssignment,
    ClaimTaskRequest,
    CreateAutomationTaskRequest,
    TaskFailureReport,
    TaskLogBatch,
    TaskProgressReport,
    TaskResultReport,
)

router = APIRouter(tags=["automation-tasks"])


@router.post("/automation/tasks")
async def create_task(
    request: CreateAutomationTaskRequest,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.create(request)


@router.get("/automation/tasks")
async def list_tasks(
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> list[AutomationTask]:
    return await service.list()


@router.get("/automation/tasks/{task_id}")
async def get_task(
    task_id: UUID,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.get(task_id)


@router.post("/device-agents/tasks/claim")
async def claim_task(
    request: ClaimTaskRequest,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTaskAssignment | None:
    return await service.claim(request)


@router.post("/automation/tasks/{task_id}/accept")
async def accept_task(
    task_id: UUID,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.accept(task_id)


@router.post("/automation/tasks/{task_id}/start")
async def start_task(
    task_id: UUID,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.start(task_id)


@router.post("/automation/tasks/{task_id}/progress")
async def progress_task(
    task_id: UUID,
    request: TaskProgressReport,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.progress(task_id, request)


@router.post("/automation/tasks/{task_id}/logs:batch")
async def batch_logs(
    task_id: UUID,
    request: TaskLogBatch,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> dict[str, int]:
    return await service.logs(task_id, request)


@router.post("/automation/tasks/{task_id}/complete")
async def complete_task(
    task_id: UUID,
    request: TaskResultReport,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.complete(task_id, request)


@router.post("/automation/tasks/{task_id}/fail")
async def fail_task(
    task_id: UUID,
    request: TaskFailureReport,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.fail(task_id, request)


@router.post("/automation/tasks/{task_id}/cancel")
async def cancel_task(
    task_id: UUID,
    service: AutomationTaskService = Depends(get_automation_task_service),
) -> AutomationTask:
    return await service.cancel(task_id)
