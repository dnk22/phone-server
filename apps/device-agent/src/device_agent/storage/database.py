import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1


class LocalDatabase:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path)
        self._connection.row_factory = sqlite3.Row
        self.bootstrap()

    def bootstrap(self) -> None:
        self._connection.execute(
            "create table if not exists meta (key text primary key, value text not null)"
        )
        self._connection.execute(
            "create table if not exists pending_logs "
            "(event_id text primary key, task_id text not null, "
            "payload text not null, sequence integer not null)"
        )
        self._connection.execute(
            "insert or replace into meta (key, value) values ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
        self._connection.commit()

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    def close(self) -> None:
        self._connection.close()
