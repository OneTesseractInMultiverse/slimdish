"""Environment-backed application configuration."""

from pathlib import Path

from envbind import BooleanEnv, IntEnv, ParameterSource, StringEnv


class Settings(ParameterSource):
    """Parse and validate process configuration once at startup."""

    environment: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_ENV", optional=True, default="development"
    )
    host: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_HOST",
        optional=True,
        default="0.0.0.0",  # noqa: S104 - server bind address, not a client address
    )
    port: int = IntEnv(  # type: ignore[assignment]  # descriptor exposes int
        envar="APP_PORT", optional=True, default=8000
    )
    database_path_value: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_DATABASE_PATH",
        optional=True,
        default="./data/slimdash.db",
    )
    session_secret: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_SESSION_SECRET",
        optional=True,
        default="development-only-change-this-secret",
    )
    public_url: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_PUBLIC_URL",
        optional=True,
        default="http://localhost:8000",
    )
    allowed_hosts_value: str = StringEnv(  # type: ignore[assignment]  # descriptor exposes str
        envar="APP_ALLOWED_HOSTS",
        optional=True,
        default="localhost,127.0.0.1,testserver",
    )
    secure_cookies: bool = BooleanEnv(  # type: ignore[assignment]  # descriptor exposes bool
        envar="APP_SECURE_COOKIES",
        optional=True,
        default=False,
    )
    oidc_client_id: str | None = StringEnv(  # type: ignore[assignment]  # descriptor
        envar="W3ID_CLIENT_ID", optional=True
    )
    oidc_client_secret: str | None = StringEnv(  # type: ignore[assignment]  # descriptor
        envar="W3ID_CLIENT_SECRET", optional=True
    )
    oidc_discovery_url: str | None = StringEnv(  # type: ignore[assignment]  # descriptor
        envar="W3ID_DISCOVERY_URL", optional=True
    )

    @property
    def database_path(self) -> Path:
        """Return the normalized SQLite file path."""
        return Path(self.database_path_value)

    @property
    def allowed_hosts(self) -> list[str]:
        """Return non-empty trusted hosts."""
        return [host.strip() for host in self.allowed_hosts_value.split(",") if host.strip()]

    @property
    def oidc_enabled(self) -> bool:
        """Return whether all OIDC settings are present."""
        values = (self.oidc_client_id, self.oidc_client_secret, self.oidc_discovery_url)
        if any(values) and not all(values):
            raise ValueError("W3ID_CLIENT_ID, W3ID_CLIENT_SECRET, and W3ID_DISCOVERY_URL are a set")
        return all(values)

    def validate_security(self) -> None:
        """Reject unsafe production configuration."""
        minimum_secret_length = 32
        if self.environment == "production" and len(self.session_secret) < minimum_secret_length:
            raise ValueError("APP_SESSION_SECRET must contain at least 32 characters")
        if self.environment == "production" and not self.secure_cookies:
            raise ValueError("APP_SECURE_COOKIES must be true in production")
