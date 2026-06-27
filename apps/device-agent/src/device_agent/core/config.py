import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DeviceAgentConfig:
    control_api_url: str = "http://127.0.0.1:8000"
    name: str = "Development Device Agent"
    configured_id: str | None = None
    token: str | None = None
    data_dir: Path = Path("./data/device-agent")
    poll_interval_seconds: float = 5
    heartbeat_interval_seconds: float = 15
    log_batch_size: int = 25
    log_flush_interval_seconds: float = 2
    request_timeout_seconds: float = 15
    enable_mock_device: bool = False
    version: str = "0.1.0"
    platform: str = "android-termux"
    architecture: str = "unknown"


def load_config() -> DeviceAgentConfig:
    return DeviceAgentConfig(
        control_api_url=os.getenv(
            "DEVICE_AGENT_CONTROL_API_URL", os.getenv("CONTROL_API_URL", "http://127.0.0.1:8000")
        ).rstrip("/"),
        name=os.getenv("DEVICE_AGENT_NAME", "Development Device Agent"),
        configured_id=os.getenv("DEVICE_AGENT_ID") or None,
        token=os.getenv("DEVICE_AGENT_TOKEN") or None,
        data_dir=Path(os.getenv("DEVICE_AGENT_DATA_DIR", "./data/device-agent")),
        poll_interval_seconds=float(os.getenv("DEVICE_AGENT_POLL_INTERVAL_SECONDS", "5")),
        heartbeat_interval_seconds=float(
            os.getenv("DEVICE_AGENT_HEARTBEAT_INTERVAL_SECONDS", "15")
        ),
        log_batch_size=int(os.getenv("DEVICE_AGENT_LOG_BATCH_SIZE", "25")),
        log_flush_interval_seconds=float(os.getenv("DEVICE_AGENT_LOG_FLUSH_INTERVAL_SECONDS", "2")),
        request_timeout_seconds=float(os.getenv("DEVICE_AGENT_REQUEST_TIMEOUT_SECONDS", "15")),
        enable_mock_device=os.getenv("DEVICE_AGENT_ENABLE_MOCK_DEVICE", "false").lower() == "true",
        architecture=os.uname().machine if hasattr(os, "uname") else "unknown",
    )
