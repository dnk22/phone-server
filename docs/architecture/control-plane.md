# Control plane

Control API is responsible for:

- agent registration and lifecycle status;
- pairing, approval, disconnect, and revoke semantics;
- heartbeat processing and offline detection;
- capability and device registry;
- readiness calculation;
- automation task orchestration and state transitions;
- structured progress and log ingestion.

The current implementation uses an in-memory repository abstraction for foundation tests. Routes call services; services call repositories. Production persistence and auth can replace these seams later without moving route logic into storage code.
