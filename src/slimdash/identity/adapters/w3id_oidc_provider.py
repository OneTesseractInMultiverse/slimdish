"""W3ID OpenID Connect adapter."""

from typing import cast

from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import Response

from slimdash.identity.domain.user import User


class W3idOidcProvider:
    """Authenticate users through an OpenID Connect discovery endpoint."""

    def __init__(self, client_id: str, client_secret: str, discovery_url: str) -> None:
        """Configure an OIDC client from discovery metadata."""
        oauth = OAuth()
        oauth.register(
            name="w3id",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=discovery_url,
            client_kwargs={"scope": "openid profile email"},
        )
        self._client = oauth.create_client("w3id")

    async def begin_login(self, request: Request, redirect_uri: str) -> Response:
        """Delegate redirect construction and state/nonce creation to Authlib."""
        if self._client is None:
            raise RuntimeError("OIDC client is unavailable")
        response = await self._client.authorize_redirect(request, redirect_uri)
        return cast("Response", response)

    async def complete_login(self, request: Request) -> User:
        """Exchange the code and map verified ID-token claims into the domain."""
        if self._client is None:
            raise RuntimeError("OIDC client is unavailable")
        token = await self._client.authorize_access_token(request)
        claims = token.get("userinfo")
        if not isinstance(claims, dict) or not isinstance(claims.get("sub"), str):
            raise TypeError("The identity provider returned no valid subject")
        subject = claims["sub"]
        name = claims.get("name")
        email = claims.get("email")
        return User(
            subject=subject,
            display_name=name if isinstance(name, str) else subject,
            email=email if isinstance(email, str) else None,
        )
