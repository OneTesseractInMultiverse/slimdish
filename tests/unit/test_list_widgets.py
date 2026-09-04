"""Tests for dashboard application behavior."""

from slimdash.dashboard.application.list_widgets import DEMO_WIDGETS, ListWidgets
from slimdash.dashboard.domain.widget import Widget


class InMemoryWidgetRepository:
    """A deterministic test adapter requiring no external setup."""

    def __init__(self, widgets: tuple[Widget, ...] = ()) -> None:
        self.widgets = widgets

    def list_all(self) -> tuple[Widget, ...]:
        return self.widgets

    def seed_if_empty(self, widgets: tuple[Widget, ...]) -> None:
        if not self.widgets:
            self.widgets = widgets

    def is_ready(self) -> bool:
        return True


def test_seeds_and_returns_demo_widgets_when_repository_is_empty() -> None:
    repository = InMemoryWidgetRepository()

    result = ListWidgets(repository).execute()

    assert result == DEMO_WIDGETS


def test_preserves_existing_widgets() -> None:
    existing = (DEMO_WIDGETS[0],)
    repository = InMemoryWidgetRepository(existing)

    result = ListWidgets(repository).execute()

    assert result == existing
