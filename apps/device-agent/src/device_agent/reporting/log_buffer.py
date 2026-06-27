import json
import sqlite3
from uuid import UUID

from contracts import TaskLogBatch, TaskLogEntry


class LogBuffer:
    def __init__(self, connection: sqlite3.Connection, *, max_entries: int = 1_000) -> None:
        self._connection = connection
        self._max_entries = max_entries

    def append(self, task_id: UUID, entry: TaskLogEntry) -> None:
        count = self._connection.execute("select count(*) from pending_logs").fetchone()[0]
        if count >= self._max_entries and entry.level != "error":
            return
        self._connection.execute(
            "insert or ignore into pending_logs "
            "(event_id, task_id, payload, sequence) values (?, ?, ?, ?)",
            (str(entry.event_id), str(task_id), entry.model_dump_json(), entry.sequence),
        )
        self._connection.commit()

    def next_batch(self, task_id: UUID, limit: int) -> TaskLogBatch:
        rows = self._connection.execute(
            "select payload from pending_logs where task_id = ? order by sequence limit ?",
            (str(task_id), limit),
        ).fetchall()
        return TaskLogBatch(
            entries=[TaskLogEntry.model_validate(json.loads(row["payload"])) for row in rows]
        )

    def acknowledge(self, entries: list[TaskLogEntry]) -> None:
        self._connection.executemany(
            "delete from pending_logs where event_id = ?",
            [(str(entry.event_id),) for entry in entries],
        )
        self._connection.commit()
