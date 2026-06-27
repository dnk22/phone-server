from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from contracts import AgentLifecycleStatus, CapabilityReport, DeviceReport


def _empty_capabilities() -> list[CapabilityReport]:
    return []


def _empty_devices() -> list[DeviceReport]:
    return []


@dataclass
class DeviceAgentRecord:
    external_id: str
    name: str
    agent_version: str
    platform: str
    architecture: str
    id: UUID = field(default_factory=uuid4)
    status: AgentLifecycleStatus = AgentLifecycleStatus.DISCOVERED
    capabilities: list[CapabilityReport] = field(default_factory=_empty_capabilities)
    devices: list[DeviceReport] = field(default_factory=_empty_devices)
    last_seen_at: datetime | None = None
    paired_at: datetime | None = None
    revoked_at: datetime | None = None
    pairing_code: str | None = None
    pairing_expires_at: datetime | None = None
    token_hash: str | None = None
