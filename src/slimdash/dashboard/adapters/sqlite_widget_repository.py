"""SQLite widget repository."""

import sqlite3
from pathlib import Path

from slimdash.dashboard.domain.widget import Widget, WidgetKind


class SqliteWidgetRepository:
    """Persist widgets in a local SQLite database."""

    def __init__(self, database_path: Path) -> None:
        """Create an adapter for one database file."""
        self._database_path = database_path

    def initialize(self) -> None:
        """Create the storage directory and schema idempotently."""
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS widgets (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    value TEXT NOT NULL,
                    kind TEXT NOT NULL CHECK(kind IN ('stat', 'progress')),
                    detail TEXT NOT NULL,
                    display_order INTEGER NOT NULL
                )
                """,
            )

    def seed_if_empty(self, widgets: tuple[Widget, ...]) -> None:
        """Insert demo records in one transaction if the table is empty."""
        with self._connect() as connection:
            count = connection.execute("SELECT COUNT(*) FROM widgets").fetchone()
            if count is not None and count[0] > 0:
                return
            connection.executemany(
                "INSERT INTO widgets VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (item.identifier, item.title, item.value, item.kind.value, item.detail, index)
                    for index, item in enumerate(widgets)
                ],
            )

    def list_all(self) -> tuple[Widget, ...]:
        """Load all widgets in their stable display order."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, title, value, kind, detail FROM widgets ORDER BY display_order",
            ).fetchall()
        return tuple(Widget(row[0], row[1], row[2], WidgetKind(row[3]), row[4]) for row in rows)

    def is_ready(self) -> bool:
        """Verify that a query can be executed."""
        try:
            with self._connect() as connection:
                connection.execute("SELECT 1").fetchone()
        except sqlite3.Error:
            return False
        return True

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection
