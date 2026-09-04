"""HTTP response representations."""

from pydantic import BaseModel, ConfigDict

from slimdash.dashboard.domain.widget import WidgetKind


class WidgetResponse(BaseModel):
    """Public widget representation."""

    model_config = ConfigDict(from_attributes=True)

    identifier: str
    title: str
    value: str
    kind: WidgetKind
    detail: str


class UserResponse(BaseModel):
    """Public authenticated-user representation."""

    authenticated: bool
    display_name: str | None = None
    email: str | None = None
