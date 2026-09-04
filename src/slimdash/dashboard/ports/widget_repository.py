"""Widget persistence boundary."""

from typing import Protocol

from slimdash.dashboard.domain.widget import Widget


class WidgetRepository(Protocol):
    """Persistence operations required by dashboard use cases."""

    def list_all(self) -> tuple[Widget, ...]:
        """Return dashboard widgets in display order."""
        ...

    def seed_if_empty(self, widgets: tuple[Widget, ...]) -> None:
        """Add initial widgets only when storage contains none."""
        ...

    def is_ready(self) -> bool:
        """Return whether persistence can accept queries."""
        ...
