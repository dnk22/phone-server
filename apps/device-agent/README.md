# Device Agent

Python worker for Android-bound automation tasks. It does not expose a FastAPI server or inbound REST API.

Run locally:

```bash
DEVICE_AGENT_ENABLE_MOCK_DEVICE=true uv run --package device-agent device-agent
```

The agent creates a persistent local identity, reports heartbeat/capabilities/devices to Control API, polls for tasks, runs a placeholder executor, and reports structured progress/log/result events.
