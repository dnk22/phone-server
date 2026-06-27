from dataclasses import dataclass
from uuid import UUID, uuid4

from contracts import DeviceReport


@dataclass
class DeviceRecord:
    agent_id: UUID
    report: DeviceReport
    id: UUID = uuid4()
