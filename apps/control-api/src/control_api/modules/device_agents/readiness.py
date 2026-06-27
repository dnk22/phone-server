from control_api.modules.device_agents.models import DeviceAgentRecord

from contracts import (
    AgentLifecycleStatus,
    AutomationReadiness,
    CapabilityStatus,
    DeviceReport,
    DeviceStatus,
)


def calculate_readiness(
    agent: DeviceAgentRecord,
    device: DeviceReport,
    *,
    effective_status: AgentLifecycleStatus,
) -> AutomationReadiness:
    reasons: list[str] = []
    if effective_status != AgentLifecycleStatus.CONNECTED:
        reasons.append("agent_not_paired")
    if agent.status == AgentLifecycleStatus.REVOKED:
        reasons.append("agent_revoked")
    if device.status not in {DeviceStatus.READY, DeviceStatus.ONLINE}:
        reasons.append("device_not_ready")
    if device.busy:
        reasons.append("device_busy")

    capability_map = {cap.name: cap.status for cap in [*agent.capabilities, *device.capabilities]}
    if capability_map.get("android.adb") != CapabilityStatus.AVAILABLE:
        if capability_map.get("android.adb") == CapabilityStatus.PERMISSION_REQUIRED:
            reasons.append("adb_permission_required")
        else:
            reasons.append("adb_unavailable")
    if capability_map.get("android.u2") != CapabilityStatus.AVAILABLE:
        reasons.append("u2_unavailable")
    return AutomationReadiness(ready=not reasons, reasons=reasons)
