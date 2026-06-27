from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

JsonObject = dict[str, object]
LogLevel = Literal["debug", "info", "warning", "error"]


def utc_now() -> datetime:
    return datetime.now(UTC)


class CommandType(StrEnum):
    TASK_CANCEL = "task.cancel"
    AGENT_REFRESH_CAPABILITIES = "agent.refresh_capabilities"
    AGENT_REFRESH_DEVICES = "agent.refresh_devices"


class AgentCommand(BaseModel):
    type: CommandType
    payload: JsonObject = Field(default_factory=dict)


class TaskLogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: UUID
    sequence: int = Field(ge=0)
    timestamp: datetime
    level: LogLevel
    event: str = Field(min_length=1, max_length=128)
    message: str = Field(max_length=4_000)
    context: JsonObject = Field(default_factory=dict)
