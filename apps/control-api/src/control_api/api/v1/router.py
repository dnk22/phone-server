from control_api.api.v1 import automation_tasks, device_agents, devices, health
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(device_agents.router)
api_router.include_router(devices.router)
api_router.include_router(automation_tasks.router)
