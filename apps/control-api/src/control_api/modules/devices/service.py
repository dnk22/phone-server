from uuid import UUID

from control_api.infrastructure.persistence.memory.repository import MemoryRepository
from control_api.modules.device_agents.readiness import calculate_readiness

from contracts import AutomationReadiness, DeviceReport


class DeviceService:
    def __init__(self, repository: MemoryRepository) -> None:
        self._repository = repository

    async def list_for_agent(self, agent_id: UUID) -> list[DeviceReport]:
        return await self._repository.list_agent_devices(agent_id)

    async def get_device(self, device_id: UUID) -> DeviceReport:
        _agent, device = await self._repository.get_device(device_id)
        return device

    async def readiness(self, device_id: UUID) -> AutomationReadiness:
        agent, device = await self._repository.get_device(device_id)
        return calculate_readiness(
            agent,
            device,
            effective_status=self._repository.effective_agent_status(agent),
        )
