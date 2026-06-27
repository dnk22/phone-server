from typing import Protocol

from device_agent.tasks.context import TaskExecutionContext

from contracts import AutomationTaskAssignment


class TaskExecutionResult:
    def __init__(
        self, succeeded: bool, result: dict[str, object], error: str | None = None
    ) -> None:
        self.succeeded = succeeded
        self.result = result
        self.error = error


class TaskExecutor(Protocol):
    task_type: str

    async def execute(
        self,
        task: AutomationTaskAssignment,
        context: TaskExecutionContext,
    ) -> TaskExecutionResult: ...
