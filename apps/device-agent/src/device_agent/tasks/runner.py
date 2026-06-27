from device_agent.client.control_api_client import ControlApiClient
from device_agent.tasks.context import TaskExecutionContext
from device_agent.tasks.registry import ExecutorRegistry

from contracts import AutomationTaskAssignment, TaskFailureReport, TaskLogBatch, TaskResultReport


class TaskRunner:
    def __init__(self, client: ControlApiClient, registry: ExecutorRegistry) -> None:
        self._client = client
        self._registry = registry

    async def run(self, assignment: AutomationTaskAssignment) -> None:
        task = assignment.task
        executor = self._registry.get("automation.run")
        context = TaskExecutionContext()
        await self._client.accept_task(task.id)
        await self._client.start_task(task.id)
        result = await executor.execute(assignment, context)
        for progress in context.progress_events:
            await self._client.report_progress(task.id, progress)
        if context.log_entries:
            await self._client.send_log_batch(task.id, TaskLogBatch(entries=context.log_entries))
        if result.succeeded:
            await self._client.complete_task(task.id, TaskResultReport(result=result.result))
        else:
            await self._client.fail_task(
                task.id,
                TaskFailureReport(error=result.error or "failed", result=result.result),
            )
