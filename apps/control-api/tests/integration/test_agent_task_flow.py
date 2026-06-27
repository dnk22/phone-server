# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from datetime import UTC, datetime
from uuid import NAMESPACE_URL, uuid4, uuid5

import httpx
from fastapi.testclient import TestClient


def register(client: TestClient, external_id: str = "agent-k20-01") -> dict[str, object]:
    response: httpx.Response = client.post(
        "/api/v1/device-agents/register",
        json={
            "agent_external_id": external_id,
            "name": "K20 Pro 01",
            "agent_version": "0.1.0",
            "platform": "android-termux",
            "architecture": "aarch64",
        },
    )
    assert response.status_code == 200
    return response.json()


def connect_agent_with_ready_device(client: TestClient) -> tuple[str, str]:
    registration = register(client)
    agent_id = str(registration["agent_id"])
    assert registration["status"] == "discovered"
    assert client.post(f"/api/v1/device-agents/{agent_id}/pair").status_code == 200
    approved = client.post(f"/api/v1/device-agents/{agent_id}/approve")
    assert approved.status_code == 200
    assert approved.json()["status"] == "connected"
    heartbeat = client.post(
        "/api/v1/device-agents/heartbeat",
        json={
            "agent_external_id": "agent-k20-01",
            "agent_version": "0.1.0",
            "status": "online",
            "current_task_ids": [],
            "capabilities": [
                {"name": "android.adb", "status": "available"},
                {"name": "android.u2", "status": "available"},
            ],
            "devices": [
                {
                    "external_id": "device-external-id",
                    "name": "Mock Device",
                    "status": "ready",
                    "busy": False,
                    "capabilities": [
                        {"name": "android.adb", "status": "available"},
                        {"name": "android.u2", "status": "available"},
                    ],
                }
            ],
            "sent_at": datetime.now(UTC).isoformat(),
        },
    )
    assert heartbeat.status_code == 200
    device_id = str(uuid5(NAMESPACE_URL, f"{agent_id}:device-external-id"))
    return agent_id, device_id


def test_health_endpoint(client: TestClient) -> None:
    response: httpx.Response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "control-api"}


def test_register_idempotent_and_revoked_agent_cannot_register(client: TestClient) -> None:
    first = register(client)
    second = register(client)
    assert first["agent_id"] == second["agent_id"]

    agent_id = first["agent_id"]
    assert client.post(f"/api/v1/device-agents/{agent_id}/revoke").status_code == 200
    rejected = client.post(
        "/api/v1/device-agents/register",
        json={
            "agent_external_id": "agent-k20-01",
            "name": "K20 Pro 01",
            "agent_version": "0.1.0",
            "platform": "android-termux",
            "architecture": "aarch64",
        },
    )
    assert rejected.status_code == 403


def test_readiness_reasons(client: TestClient) -> None:
    _agent_id, device_id = connect_agent_with_ready_device(client)
    ready = client.get(f"/api/v1/devices/{device_id}/readiness")

    assert ready.status_code == 200
    assert ready.json() == {"ready": True, "reasons": []}


def test_task_claim_and_complete_flow_deduplicates_logs(client: TestClient) -> None:
    _agent_id, device_id = connect_agent_with_ready_device(client)
    create_response = client.post(
        "/api/v1/automation/tasks",
        json={
            "target_device_id": device_id,
            "scenario_id": "scenario-placeholder",
            "scenario_version": 1,
            "payload": {},
            "required_capabilities": ["android.adb", "android.u2"],
        },
    )
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    claim_response = client.post(
        "/api/v1/device-agents/tasks/claim",
        json={
            "agent_external_id": "agent-k20-01",
            "available_device_ids": ["device-external-id"],
            "max_tasks": 1,
        },
    )
    assert claim_response.status_code == 200
    assert claim_response.json()["task"]["id"] == task_id
    assert client.post(f"/api/v1/automation/tasks/{task_id}/accept").json()["status"] == "accepted"
    assert client.post(f"/api/v1/automation/tasks/{task_id}/start").json()["status"] == "running"
    progress = client.post(
        f"/api/v1/automation/tasks/{task_id}/progress",
        json={
            "progress": 45,
            "current_step": 5,
            "total_steps": 11,
            "message": "Running placeholder automation",
        },
    )
    assert progress.status_code == 200
    event_id = str(uuid4())
    logs = client.post(
        f"/api/v1/automation/tasks/{task_id}/logs:batch",
        json={
            "entries": [
                {
                    "event_id": event_id,
                    "sequence": 1,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "level": "info",
                    "event": "task.started",
                    "message": "Task started",
                    "context": {},
                },
                {
                    "event_id": event_id,
                    "sequence": 1,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "level": "info",
                    "event": "task.started",
                    "message": "Task started",
                    "context": {},
                },
            ]
        },
    )
    assert logs.json() == {"accepted": 2, "stored": 1}
    complete = client.post(
        f"/api/v1/automation/tasks/{task_id}/complete", json={"result": {"ok": True}}
    )
    assert complete.status_code == 200
    assert complete.json()["status"] == "succeeded"


def test_unpaired_or_wrong_capability_agents_do_not_claim(client: TestClient) -> None:
    register(client)
    claim = client.post(
        "/api/v1/device-agents/tasks/claim",
        json={
            "agent_external_id": "agent-k20-01",
            "available_device_ids": ["device-external-id"],
            "max_tasks": 1,
        },
    )
    assert claim.json() is None
