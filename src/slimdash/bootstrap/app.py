"""FastAPI composition root."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from slimdash.bootstrap.config import Settings
from slimdash.dashboard.adapters.sqlite_widget_repository import SqliteWidgetRepository
from slimdash.dashboard.application.list_widgets import ListWidgets
from slimdash.identity.adapters.w3id_oidc_provider import W3idOidcProvider
from slimdash.identity.ports.identity_provider import IdentityProvider
from slimdash.web.routes import create_api_router, create_auth_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Compose the application using replaceable adapters."""
    config = settings or Settings()
    config.validate_security()
    repository = SqliteWidgetRepository(config.database_path)
    provider = _build_identity_provider(config)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        repository.initialize()
        yield

    app = FastAPI(title="SlimDash", version="0.1.0", lifespan=lifespan)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.session_secret,
        session_cookie="slimdash_session",
        same_site="lax",
        https_only=config.secure_cookies,
        max_age=3600,
    )

    @app.middleware("http")
    async def security_headers(request: Request, call_next: object) -> Response:
        response: Response = await call_next(request)  # type: ignore[operator]
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; connect-src 'self'"
        )
        return response

    app.include_router(create_api_router(ListWidgets(repository), repository))
    app.include_router(create_auth_router(provider, config.public_url))
    _mount_frontend(app)
    return app


def _build_identity_provider(settings: Settings) -> IdentityProvider | None:
    if not settings.oidc_enabled:
        return None
    if (
        not settings.oidc_client_id
        or not settings.oidc_client_secret
        or not settings.oidc_discovery_url
    ):
        raise ValueError("OIDC configuration is incomplete")
    return W3idOidcProvider(
        settings.oidc_client_id,
        settings.oidc_client_secret,
        settings.oidc_discovery_url,
    )


def _mount_frontend(app: FastAPI) -> None:
    static_dir = Path(__file__).resolve().parents[3] / "static"
    assets_dir = static_dir / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def single_page_app(path: str) -> FileResponse:
        requested_file = static_dir / path
        if path and requested_file.is_file() and static_dir in requested_file.resolve().parents:
            return FileResponse(requested_file)
        return FileResponse(static_dir / "index.html")


app = create_app()
