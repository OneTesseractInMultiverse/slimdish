"""External identity provider boundary."""

from typing import Protocol

from starlette.requests import Request
from starlette.responses import Response

from slimdash.identity.domain.user import User


class IdentityProvider(Protocol):
    """OIDC operations required by the inbound web adapter."""

    async def begin_login(self, request: Request, redirect_uri: str) -> Response:
        """Start the authorization-code flow."""
        ...

    async def complete_login(self, request: Request) -> User:
        """Validate the callback and return a minimal identity."""
        ...
