from functools import lru_cache

from control_api.core.config import ControlApiSettings, load_settings
from control_api.infrastructure.persistence.memory.repository import MemoryRepository
from control_api.modules.automation_tasks.service import AutomationTaskService
from control_api.modules.device_agents.service import DeviceAgentService
from control_api.modules.devices.service import DeviceService


@lru_cache(maxsize=1)
def get_settings() -> ControlApiSettings:
    return load_settings()


@lru_cache(maxsize=1)
def get_repository() -> MemoryRepository:
    settings = get_settings()
    return MemoryRepository(heartbeat_timeout_seconds=settings.heartbeat_timeout_seconds)


def get_device_agent_service() -> DeviceAgentService:
    return DeviceAgentService(get_repository(), get_settings())


def get_device_service() -> DeviceService:
    return DeviceService(get_repository())


def get_automation_task_service() -> AutomationTaskService:
    return AutomationTaskService(get_repository())


def reset_dependencies_for_tests() -> None:
    get_settings.cache_clear()
    get_repository.cache_clear()
