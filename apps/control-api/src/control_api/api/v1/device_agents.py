# ruff: noqa: B008
from uuid import UUID

from control_api.api.dependencies import get_device_agent_service, get_device_service
from control_api.modules.device_agents.service import DeviceAgentService
from control_api.modules.devices.service import DeviceService
from fastapi import APIRouter, Depends, Query

from contracts import (
    AgentHeartbeatRequest,
    AgentHeartbeatResponse,
    AgentLifecycleStatus,
    AgentRegistrationRequest,
    AgentRegistrationResponse,
    AgentSummary,
    DeviceReport,
)

router = APIRouter(prefix="/device-agents", tags=["device-agents"])


@router.post("/register")
async def register_agent(
    request: AgentRegistrationRequest,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentRegistrationResponse:
    return await service.register(request)


@router.post("/heartbeat")
async def heartbeat(
    request: AgentHeartbeatRequest,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentHeartbeatResponse:
    return await service.heartbeat(request)


@router.get("")
async def list_agents(
    status: AgentLifecycleStatus | None = Query(default=None),
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> list[AgentSummary]:
    return await service.list_agents(status)


@router.get("/{agent_id}")
async def get_agent(
    agent_id: UUID,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentSummary:
    return await service.get_agent(agent_id)


@router.post("/{agent_id}/pair")
async def start_pairing(
    agent_id: UUID,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentSummary:
    return await service.start_pairing(agent_id)


@router.post("/{agent_id}/approve")
async def approve_pairing(
    agent_id: UUID,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentSummary:
    return await service.approve(agent_id)


@router.post("/{agent_id}/disconnect")
async def disconnect_agent(
    agent_id: UUID,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentSummary:
    return await service.disconnect(agent_id)


@router.post("/{agent_id}/revoke")
async def revoke_agent(
    agent_id: UUID,
    service: DeviceAgentService = Depends(get_device_agent_service),
) -> AgentSummary:
    return await service.revoke(agent_id)


@router.get("/{agent_id}/devices")
async def list_agent_devices(
    agent_id: UUID,
    service: DeviceService = Depends(get_device_service),
) -> list[DeviceReport]:
    return await service.list_for_agent(agent_id)
