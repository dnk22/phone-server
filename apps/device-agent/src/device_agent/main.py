import asyncio
import signal
from contextlib import suppress

from contracts import (
    AgentHeartbeatRequest,
    AgentLifecycleStatus,
    AgentRegistrationRequest,
    ClaimTaskRequest,
    utc_now,
)
from device_agent.capabilities.detector import CapabilityDetector
from device_agent.client.control_api_client import ControlApiClient
from device_agent.core.config import load_config
from device_agent.core.identity import load_or_create_agent_id
from device_agent.core.lifecycle import ShutdownToken
from device_agent.devices.discovery import DeviceDiscovery
from device_agent.storage.database import LocalDatabase
from device_agent.tasks.registry import default_registry
from device_agent.tasks.runner import TaskRunner


async def run_worker() -> None:
    config = load_config()
    agent_id = load_or_create_agent_id(config.data_dir, config.configured_id)
    database = LocalDatabase(config.data_dir / "device-agent.sqlite3")
    shutdown = ShutdownToken()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError):
            loop.add_signal_handler(sig, shutdown.request_shutdown)

    detector = CapabilityDetector()
    discovery = DeviceDiscovery(enable_mock_device=config.enable_mock_device)
    async with ControlApiClient(
        config.control_api_url,
        timeout_seconds=config.request_timeout_seconds,
    ) as client:
        await client.register_agent(
            AgentRegistrationRequest(
                agent_external_id=agent_id,
                name=config.name,
                agent_version=config.version,
                platform=config.platform,
                architecture=config.architecture,
            )
        )
        runner = TaskRunner(client, default_registry())
        while not shutdown.requested:
            capabilities = detector.detect()
            devices = await discovery.discover()
            heartbeat = await client.send_heartbeat(
                AgentHeartbeatRequest(
                    agent_external_id=agent_id,
                    agent_version=config.version,
                    current_task_ids=[],
                    capabilities=capabilities,
                    devices=devices,
                    sent_at=utc_now(),
                )
            )
            if heartbeat.agent_status == AgentLifecycleStatus.CONNECTED and devices:
                assignment = await client.claim_task(
                    ClaimTaskRequest(
                        agent_external_id=agent_id,
                        available_device_ids=[device.external_id for device in devices],
                    )
                )
                if assignment is not None:
                    await runner.run(assignment)
            await shutdown.wait(config.poll_interval_seconds)
    database.close()


def main() -> None:
    asyncio.run(run_worker())
