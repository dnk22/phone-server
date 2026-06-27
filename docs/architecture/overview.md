# Architecture overview

```text
Dashboard → Control API → Device Agent → Android device
```

Control API is the control plane. It exposes REST APIs for the dashboard and outbound-polling Device Agents, owns central state, and computes automation readiness.

Device Agent is the execution plane. It runs close to Android devices, reports local capability/device state, claims approved tasks, and sends structured progress/log/result events back to Control API.

The MVP intentionally avoids inbound agent connectivity: Control API never calls a Device Agent IP, and Device Agent never exposes a FastAPI server.
