# Control API

FastAPI control plane for device-agent registration, pairing, heartbeat, device reporting, readiness checks, and automation task orchestration.

Run locally:

```bash
uv run uvicorn control_api.main:app --app-dir apps/control-api/src --reload --host 127.0.0.1 --port 8000
```

The MVP uses an in-process repository abstraction. Production persistence is intentionally deferred.
