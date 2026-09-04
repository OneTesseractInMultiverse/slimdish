"""Authenticated user model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """Minimal identity exposed to the application."""

    subject: str
    display_name: str
    email: str | None = None
