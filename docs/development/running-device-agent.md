# Running Device Agent

Local foundation run:

```bash
make dev-control-api
DEVICE_AGENT_ENABLE_MOCK_DEVICE=true make dev-device-agent
```

Useful environment variables:

```env
DEVICE_AGENT_CONTROL_API_URL=http://127.0.0.1:8000
DEVICE_AGENT_NAME=Development Device Agent
DEVICE_AGENT_ID=
DEVICE_AGENT_DATA_DIR=./data/device-agent
DEVICE_AGENT_ENABLE_MOCK_DEVICE=true
```

The foundation does not require a real Android device, ADB, or UIAutomator2. The mock device path is for exercising registration, heartbeat, readiness, and task polling locally.
