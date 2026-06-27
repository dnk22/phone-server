from uuid import UUID

import httpx
from device_agent.client.errors import ControlApiRequestError
from device_agent.client.retry import with_retry
from pydantic import TypeAdapter

from contracts import (
    AgentHeartbeatRequest,
    AgentHeartbeatResponse,
    AgentRegistrationRequest,
    AgentRegistrationResponse,
    AutomationTaskAssignment,
    ClaimTaskRequest,
    TaskFailureReport,
    TaskLogBatch,
    TaskProgressReport,
    TaskResultReport,
)


class ControlApiClient:
    def __init__(self, base_url: str, *, timeout_seconds: float = 15) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout_seconds)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "ControlApiClient":
        return self

    async def __aexit__(self, *_args: object) -> None:
        await self.close()

    async def register_agent(self, request: AgentRegistrationRequest) -> AgentRegistrationResponse:
        response = await with_retry(
            lambda: self._client.post(
                "/api/v1/device-agents/register",
                json=request.model_dump(mode="json"),
            )
        )
        return self._parse(response, AgentRegistrationResponse)

    async def send_heartbeat(self, request: AgentHeartbeatRequest) -> AgentHeartbeatResponse:
        response = await with_retry(
            lambda: self._client.post(
                "/api/v1/device-agents/heartbeat",
                json=request.model_dump(mode="json"),
            )
        )
        return self._parse(response, AgentHeartbeatResponse)

    async def claim_task(self, request: ClaimTaskRequest) -> AutomationTaskAssignment | None:
        response = await with_retry(
            lambda: self._client.post(
                "/api/v1/device-agents/tasks/claim",
                json=request.model_dump(mode="json"),
            )
        )
        if response.status_code >= 400:
            raise ControlApiRequestError(response.text)
        data = response.json()
        if data is None:
            return None
        return AutomationTaskAssignment.model_validate(data)

    async def accept_task(self, task_id: UUID) -> None:
        await self._post_ok(f"/api/v1/automation/tasks/{task_id}/accept", {})

    async def start_task(self, task_id: UUID) -> None:
        await self._post_ok(f"/api/v1/automation/tasks/{task_id}/start", {})

    async def report_progress(self, task_id: UUID, report: TaskProgressReport) -> None:
        await self._post_ok(
            f"/api/v1/automation/tasks/{task_id}/progress",
            report.model_dump(mode="json"),
        )

    async def send_log_batch(self, task_id: UUID, batch: TaskLogBatch) -> None:
        await self._post_ok(
            f"/api/v1/automation/tasks/{task_id}/logs:batch",
            batch.model_dump(mode="json"),
        )

    async def complete_task(self, task_id: UUID, report: TaskResultReport) -> None:
        await self._post_ok(
            f"/api/v1/automation/tasks/{task_id}/complete",
            report.model_dump(mode="json"),
        )

    async def fail_task(self, task_id: UUID, report: TaskFailureReport) -> None:
        await self._post_ok(
            f"/api/v1/automation/tasks/{task_id}/fail",
            report.model_dump(mode="json"),
        )

    async def _post_ok(self, path: str, payload: object) -> None:
        response = await self._client.post(path, json=payload)
        if response.status_code >= 400:
            raise ControlApiRequestError(response.text)

    def _parse[T](self, response: httpx.Response, model: type[T]) -> T:
        if response.status_code >= 400:
            raise ControlApiRequestError(response.text)
        return TypeAdapter(model).validate_python(response.json())
