from enum import StrEnum

from pydantic import BaseModel


class HealthState(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    ERROR = "error"


class HealthResponse(BaseModel):
    status: HealthState
    service: str = "control-api"
