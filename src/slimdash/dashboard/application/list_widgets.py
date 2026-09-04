"""List-dashboard-widgets use case."""

from slimdash.dashboard.domain.widget import Widget, WidgetKind
from slimdash.dashboard.ports.widget_repository import WidgetRepository

DEMO_WIDGETS = (
    Widget("active-projects", "Active projects", "12", WidgetKind.STAT, "+2 this month"),
    Widget("delivery-health", "Delivery health", "84%", WidgetKind.PROGRESS, "Target: 90%"),
)


class ListWidgets:
    """Retrieve the widgets visible on the dashboard."""

    def __init__(self, repository: WidgetRepository) -> None:
        """Create the use case with its persistence boundary."""
        self._repository = repository

    def execute(self) -> tuple[Widget, ...]:
        """Return all widgets, initializing generic demo content when necessary."""
        self._repository.seed_if_empty(DEMO_WIDGETS)
        return self._repository.list_all()
