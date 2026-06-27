from device_agent.executors.automation_placeholder import PlaceholderAutomationExecutor
from device_agent.executors.base import TaskExecutor


class ExecutorRegistry:
    def __init__(self) -> None:
        self._executors: dict[str, TaskExecutor] = {}

    def register(self, executor: TaskExecutor) -> None:
        self._executors[executor.task_type] = executor

    def get(self, task_type: str) -> TaskExecutor:
        return self._executors[task_type]


def default_registry() -> ExecutorRegistry:
    registry = ExecutorRegistry()
    registry.register(PlaceholderAutomationExecutor())
    return registry
