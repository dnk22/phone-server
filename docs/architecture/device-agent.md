# Device Agent

Device Agent is a Python worker, not a web server.

Lifecycle:

1. Load configuration.
2. Load or create persistent local agent identity.
3. Initialize local SQLite state.
4. Register with Control API.
5. Send heartbeat with capability and device reports.
6. If paired and idle, poll/claim a task.
7. Execute through a task executor abstraction.
8. Report progress, structured logs, and result.
9. Shut down gracefully on SIGINT/SIGTERM where supported.

The agent only performs device-bound automation work. Portable services such as download processing, ad filtering, and business workflows belong in Control API later.
