# ruff: noqa: B008
from uuid import UUID

from control_api.api.dependencies import get_device_service
from control_api.modules.devices.service import DeviceService
from fastapi import APIRouter, Depends

from contracts import AutomationReadiness, DeviceReport

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/{device_id}")
async def get_device(
    device_id: UUID,
    service: DeviceService = Depends(get_device_service),
) -> DeviceReport:
    return await service.get_device(device_id)


@router.get("/{device_id}/readiness")
async def get_device_readiness(
    device_id: UUID,
    service: DeviceService = Depends(get_device_service),
) -> AutomationReadiness:
    return await service.readiness(device_id)
