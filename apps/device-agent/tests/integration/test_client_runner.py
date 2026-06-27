import asyncio
from uuid import uuid4

import httpx
from device_agent.client.control_api_client import ControlApiClient
from device_agent.tasks.registry import default_registry
from device_agent.tasks.runner import TaskRunner

from contracts import AutomationTask, AutomationTaskAssignment, AutomationTaskStatus, utc_now


def test_runner_calls_control_api_task_lifecycle() -> None:
    asyncio.run(_run_runner_test())


async def _run_runner_test() -> None:
    calls: list[str] = []
    task = AutomationTask(
        id=uuid4(),
        target_device_id=uuid4(),
        scenario_id="scenario-placeholder",
        scenario_version=1,
        payload={},
        required_capabilities=[],
        status=AutomationTaskStatus.ASSIGNED,
        created_at=utc_now(),
        updated_at=utc_now(),
    )

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(200, json={"ok": True})

    client = ControlApiClient("http://control-api.test")
    await client._client.aclose()  # pyright: ignore[reportPrivateUsage]
    client._client = httpx.AsyncClient(  # pyright: ignore[reportPrivateUsage]
        base_url="http://control-api.test",
        transport=httpx.MockTransport(handler),
    )

    await TaskRunner(client, default_registry()).run(AutomationTaskAssignment(task=task))

    assert calls == [
        f"/api/v1/automation/tasks/{task.id}/accept",
        f"/api/v1/automation/tasks/{task.id}/start",
        f"/api/v1/automation/tasks/{task.id}/progress",
        f"/api/v1/automation/tasks/{task.id}/progress",
        f"/api/v1/automation/tasks/{task.id}/progress",
        f"/api/v1/automation/tasks/{task.id}/logs:batch",
        f"/api/v1/automation/tasks/{task.id}/complete",
    ]
    await client.close()
