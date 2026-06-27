from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from contracts.capabilities import CapabilityReport


def _empty_capabilities() -> list[CapabilityReport]:
    return []


class DeviceStatus(StrEnum):
    UNKNOWN = "unknown"
    ONLINE = "online"
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


class DeviceReport(BaseModel):
    external_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=128)
    manufacturer: str | None = None
    model: str | None = None
    android_version: str | None = None
    serial: str | None = None
    resolution: str | None = None
    status: DeviceStatus = DeviceStatus.UNKNOWN
    busy: bool = False
    current_task_id: UUID | None = None
    capabilities: list[CapabilityReport] = Field(default_factory=_empty_capabilities)


class AutomationReadiness(BaseModel):
    ready: bool
    reasons: list[str] = Field(default_factory=list)
