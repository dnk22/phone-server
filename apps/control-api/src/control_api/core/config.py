import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ControlApiSettings:
    host: str = "127.0.0.1"
    port: int = 8000
    heartbeat_timeout_seconds: int = 60
    pairing_code_ttl_seconds: int = 600
    heartbeat_interval_seconds: int = 15


def load_settings() -> ControlApiSettings:
    return ControlApiSettings(
        host=os.getenv("CONTROL_API_HOST", "127.0.0.1"),
        port=int(os.getenv("CONTROL_API_PORT", "8000")),
        heartbeat_timeout_seconds=int(
            os.getenv("CONTROL_API_AGENT_HEARTBEAT_TIMEOUT_SECONDS", "60")
        ),
        pairing_code_ttl_seconds=int(os.getenv("CONTROL_API_PAIRING_CODE_TTL_SECONDS", "600")),
        heartbeat_interval_seconds=int(os.getenv("DEVICE_AGENT_HEARTBEAT_INTERVAL_SECONDS", "15")),
    )
