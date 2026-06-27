from dataclasses import dataclass, field

from contracts import TaskLogEntry, TaskProgressReport


def _empty_progress_events() -> list[TaskProgressReport]:
    return []


def _empty_log_entries() -> list[TaskLogEntry]:
    return []


@dataclass
class TaskExecutionContext:
    progress_events: list[TaskProgressReport] = field(default_factory=_empty_progress_events)
    log_entries: list[TaskLogEntry] = field(default_factory=_empty_log_entries)
    cancelled: bool = False
