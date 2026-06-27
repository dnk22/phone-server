from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from contracts.common import JsonObject, TaskLogEntry


def _default_required_capabilities() -> list[str]:
    return ["android.adb", "android.u2"]


def _empty_log_entries() -> list[TaskLogEntry]:
    return []


class AutomationTaskStatus(StrEnum):
    PENDING = "pending"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


class CreateAutomationTaskRequest(BaseModel):
    target_device_id: UUID
    scenario_id: str = Field(min_length=1, max_length=128)
    scenario_version: int = Field(ge=1)
    payload: JsonObject = Field(default_factory=dict)
    required_capabilities: list[str] = Field(default_factory=_default_required_capabilities)


class AutomationTask(BaseModel):
    id: UUID
    target_device_id: UUID
    agent_id: UUID | None = None
    scenario_id: str
    scenario_version: int
    payload: JsonObject
    required_capabilities: list[str]
    status: AutomationTaskStatus
    progress: int = Field(default=0, ge=0, le=100)
    result: JsonObject | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime


class ClaimTaskRequest(BaseModel):
    agent_external_id: str = Field(min_length=1, max_length=128)
    available_device_ids: list[str] = Field(default_factory=list)
    max_tasks: int = Field(default=1, ge=1, le=5)


class AutomationTaskAssignment(BaseModel):
    task: AutomationTask


class TaskProgressReport(BaseModel):
    progress: int = Field(ge=0, le=100)
    current_step: int | None = Field(default=None, ge=0)
    total_steps: int | None = Field(default=None, ge=0)
    message: str | None = Field(default=None, max_length=1_000)


class TaskLogBatch(BaseModel):
    entries: list[TaskLogEntry] = Field(default_factory=_empty_log_entries, max_length=100)


class TaskResultReport(BaseModel):
    result: JsonObject = Field(default_factory=dict)


class TaskFailureReport(BaseModel):
    error: str = Field(min_length=1, max_length=2_000)
    result: JsonObject = Field(default_factory=dict)
