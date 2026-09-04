"""Widget domain objects."""

from dataclasses import dataclass
from enum import StrEnum


class WidgetKind(StrEnum):
    """Supported demo visualization types."""

    STAT = "stat"
    PROGRESS = "progress"


@dataclass(frozen=True, slots=True)
class Widget:
    """A dashboard widget independent of storage and delivery concerns."""

    identifier: str
    title: str
    value: str
    kind: WidgetKind
    detail: str
