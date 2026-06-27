from pathlib import Path
from uuid import uuid4

from device_agent.reporting.log_buffer import LogBuffer
from device_agent.storage.database import LocalDatabase

from contracts import TaskLogEntry, utc_now


def test_log_buffer_batches_and_acknowledges(tmp_path: Path) -> None:
    database = LocalDatabase(tmp_path / "agent.sqlite3")
    buffer = LogBuffer(database.connection)
    task_id = uuid4()
    entry = TaskLogEntry(
        event_id=uuid4(),
        sequence=1,
        timestamp=utc_now(),
        level="info",
        event="task.started",
        message="Task started",
        context={},
    )

    buffer.append(task_id, entry)
    batch = buffer.next_batch(task_id, limit=25)
    assert batch.entries == [entry]
    buffer.acknowledge(batch.entries)
    assert buffer.next_batch(task_id, limit=25).entries == []
    database.close()
