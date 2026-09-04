"""Tests for the SQLite adapter using pytest's isolated temporary directory."""

from pathlib import Path

from slimdash.dashboard.adapters.sqlite_widget_repository import SqliteWidgetRepository
from slimdash.dashboard.application.list_widgets import DEMO_WIDGETS


def test_initializes_seeds_and_reads_widgets(tmp_path: Path) -> None:
    repository = SqliteWidgetRepository(tmp_path / "nested" / "dashboard.db")

    repository.initialize()
    repository.seed_if_empty(DEMO_WIDGETS)

    assert repository.list_all() == DEMO_WIDGETS
    assert repository.is_ready()


def test_seed_is_idempotent(tmp_path: Path) -> None:
    repository = SqliteWidgetRepository(tmp_path / "dashboard.db")
    repository.initialize()

    repository.seed_if_empty(DEMO_WIDGETS)
    repository.seed_if_empty((DEMO_WIDGETS[0],))

    assert repository.list_all() == DEMO_WIDGETS


def test_reports_not_ready_for_missing_parent(tmp_path: Path) -> None:
    repository = SqliteWidgetRepository(tmp_path / "missing" / "dashboard.db")

    assert not repository.is_ready()
