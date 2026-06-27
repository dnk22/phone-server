from fastapi import APIRouter

from contracts import HealthResponse, HealthState

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status=HealthState.OK, service="control-api")
