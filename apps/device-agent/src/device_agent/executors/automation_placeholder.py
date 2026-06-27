from uuid import uuid4

from device_agent.executors.base import TaskExecutionResult
from device_agent.tasks.context import TaskExecutionContext

from contracts import AutomationTaskAssignment, TaskLogEntry, TaskProgressReport, utc_now


class PlaceholderAutomationExecutor:
    task_type = "automation.run"

    async def execute(
        self, task: AutomationTaskAssignment, context: TaskExecutionContext
    ) -> TaskExecutionResult:
        for sequence, progress in enumerate((10, 50, 100), start=1):
            if context.cancelled:
                return TaskExecutionResult(False, {}, "cancelled")
            context.progress_events.append(
                TaskProgressReport(
                    progress=progress,
                    current_step=sequence,
                    total_steps=3,
                    message="Running placeholder automation",
                )
            )
            context.log_entries.append(
                TaskLogEntry(
                    event_id=uuid4(),
                    sequence=sequence,
                    timestamp=utc_now(),
                    level="info",
                    event="task.placeholder_progress",
                    message=f"Placeholder progress {progress}",
                    context={"task_id": str(task.task.id)},
                )
            )
        return TaskExecutionResult(True, {"placeholder": True})
