from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from contracts import AutomationTaskStatus, TaskLogEntry, utc_now


def _empty_log_entries() -> list[TaskLogEntry]:
    return []


def _empty_log_event_ids() -> set[str]:
    return set()


@dataclass
class AutomationTaskRecord:
    target_device_id: UUID
    scenario_id: str
    scenario_version: int
    payload: dict[str, object]
    required_capabilities: list[str]
    id: UUID = field(default_factory=uuid4)
    agent_id: UUID | None = None
    status: AutomationTaskStatus = AutomationTaskStatus.QUEUED
    progress: int = 0
    result: dict[str, object] | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    assigned_at: datetime | None = None
    log_entries: list[TaskLogEntry] = field(default_factory=_empty_log_entries)
    log_event_ids: set[str] = field(default_factory=_empty_log_event_ids)
