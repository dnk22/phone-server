import asyncio
from uuid import uuid4

from device_agent.executors.automation_placeholder import PlaceholderAutomationExecutor
from device_agent.tasks.context import TaskExecutionContext

from contracts import AutomationTask, AutomationTaskAssignment, AutomationTaskStatus, utc_now


def test_placeholder_executor_emits_progress_logs_and_result() -> None:
    asyncio.run(_run_executor_test())


async def _run_executor_test() -> None:
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
    context = TaskExecutionContext()

    result = await PlaceholderAutomationExecutor().execute(
        AutomationTaskAssignment(task=task), context
    )

    assert result.succeeded is True
    assert len(context.progress_events) == 3
    assert len(context.log_entries) == 3
