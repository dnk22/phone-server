from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from contracts.capabilities import CapabilityReport
from contracts.common import AgentCommand
from contracts.devices import DeviceReport


def _empty_task_ids() -> list[UUID]:
    return []


def _empty_capabilities() -> list[CapabilityReport]:
    return []


def _empty_devices() -> list[DeviceReport]:
    return []


def _empty_commands() -> list[AgentCommand]:
    return []


class AgentLifecycleStatus(StrEnum):
    DISCOVERED = "discovered"
    PENDING_PAIRING = "pending_pairing"
    CONNECTED = "connected"
    OFFLINE = "offline"
    REVOKED = "revoked"
    ERROR = "error"


class AgentRegistrationRequest(BaseModel):
    agent_external_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=128)
    agent_version: str = Field(min_length=1, max_length=64)
    platform: str = Field(min_length=1, max_length=64)
    architecture: str = Field(min_length=1, max_length=64)


class AgentRegistrationResponse(BaseModel):
    agent_id: UUID
    agent_external_id: str
    status: AgentLifecycleStatus
    pairing_code: str | None = None
    heartbeat_interval_seconds: int
    server_time: datetime


class AgentHeartbeatRequest(BaseModel):
    agent_external_id: str = Field(min_length=1, max_length=128)
    agent_version: str = Field(min_length=1, max_length=64)
    status: str = "online"
    current_task_ids: list[UUID] = Field(default_factory=_empty_task_ids)
    capabilities: list[CapabilityReport] = Field(default_factory=_empty_capabilities)
    devices: list[DeviceReport] = Field(default_factory=_empty_devices)
    sent_at: datetime


class AgentHeartbeatResponse(BaseModel):
    agent_status: AgentLifecycleStatus
    server_time: datetime
    next_heartbeat_seconds: int
    commands: list[AgentCommand] = Field(default_factory=_empty_commands)


class AgentSummary(BaseModel):
    id: UUID
    external_id: str
    name: str
    status: AgentLifecycleStatus
    effective_status: AgentLifecycleStatus
    agent_version: str
    platform: str
    architecture: str
    last_seen_at: datetime | None = None
    paired_at: datetime | None = None
    revoked_at: datetime | None = None
