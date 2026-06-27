from enum import StrEnum

from pydantic import BaseModel, Field


class CapabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"
    BUSY = "busy"
    MISCONFIGURED = "misconfigured"
    PERMISSION_REQUIRED = "permission_required"


class CapabilityReport(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    status: CapabilityStatus
    version: str | None = None
    message: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)
