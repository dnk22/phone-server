# Android Linux Server

Monorepo foundation for an Android automation control plane:

```text
Vercel Dashboard → Control API → Device Agent → Android device
```

Control API is the FastAPI control plane. It owns agent registry, pairing/trust state, device registry, readiness calculation, automation task state, progress, and structured task logs.

Device Agent is the outbound execution plane. It is a long-running Python worker that registers with Control API, sends heartbeat/capability/device reports, polls for tasks, and reports progress/log/result events. It does not open an inbound API and does not access the central database.

## Repository layout

```text
apps/dashboard       React/Vite dashboard foundation
apps/control-api     FastAPI Control API
apps/device-agent    Python Device Agent worker
python-packages      Shared Python common/contracts/observability packages
packages             Shared TypeScript packages
docs                 Architecture, API, and development notes
tooling              Local scripts
```

## Development

```bash
make install
make dev-control-api
make dev-device-agent
make test-control-api
make test-device-agent
make check
```

`make dev` runs the dashboard and Control API. `make dev-backend` runs Control API plus a local Device Agent with mock device reporting.

## MVP boundaries

Implemented now: registration, heartbeat, pairing/approval/revoke, device/capability reports, readiness calculation, task create/claim/accept/start/progress/log/complete/fail/cancel foundation, shared Pydantic contracts, and Device Agent placeholder execution.

Deferred: real ADB/UIAutomator2 execution, screenshots, scenario engine, yt-dlp/FFmpeg/ad filtering, PostgreSQL, Redis, WebSockets, frontend UX for pairing/tasks, cloud deployment, and agent auto-update.
