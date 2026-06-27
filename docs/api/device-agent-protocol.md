# Device Agent protocol

Base path: `/api/v1`.

Agent self-service endpoints:

- `POST /device-agents/register`
- `POST /device-agents/heartbeat`
- `POST /device-agents/tasks/claim`

Dashboard/control endpoints:

- `GET /device-agents?status=discovered`
- `GET /device-agents/{agent_id}`
- `POST /device-agents/{agent_id}/pair`
- `POST /device-agents/{agent_id}/approve`
- `POST /device-agents/{agent_id}/disconnect`
- `POST /device-agents/{agent_id}/revoke`
- `GET /device-agents/{agent_id}/devices`
- `GET /devices/{device_id}`
- `GET /devices/{device_id}/readiness`

Automation task endpoints:

- `POST /automation/tasks`
- `GET /automation/tasks`
- `GET /automation/tasks/{task_id}`
- `POST /automation/tasks/{task_id}/accept`
- `POST /automation/tasks/{task_id}/start`
- `POST /automation/tasks/{task_id}/progress`
- `POST /automation/tasks/{task_id}/logs:batch`
- `POST /automation/tasks/{task_id}/complete`
- `POST /automation/tasks/{task_id}/fail`
- `POST /automation/tasks/{task_id}/cancel`

Shared request/response models live in `python-packages/contracts`.
