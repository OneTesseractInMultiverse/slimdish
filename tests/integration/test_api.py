"""In-process HTTP tests with isolated SQLite storage."""

from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from slimdash.bootstrap.app import create_app
from slimdash.bootstrap.config import Settings


def build_settings(database_path: Path) -> Settings:
    """Build settings without depending on the developer's environment."""
    with patch.dict(
        "os.environ",
        {
            "APP_DATABASE_PATH": str(database_path),
            "APP_ALLOWED_HOSTS": "testserver",
            "APP_SESSION_SECRET": "test-secret-long-enough-for-signed-cookies",
        },
        clear=True,
    ):
        return Settings()


def test_dashboard_api_and_health_endpoints(tmp_path: Path) -> None:
    with TestClient(create_app(build_settings(tmp_path / "api.db"))) as client:
        widgets = client.get("/api/widgets")
        live = client.get("/api/health/live")
        ready = client.get("/api/health/ready")

    assert widgets.status_code == 200
    assert len(widgets.json()) == 2
    assert live.json() == {"status": "ok"}
    assert ready.json() == {"status": "ready"}
    assert widgets.headers["x-content-type-options"] == "nosniff"


def test_authentication_is_optional_and_session_starts_anonymous(tmp_path: Path) -> None:
    with TestClient(create_app(build_settings(tmp_path / "auth.db"))) as client:
        user = client.get("/auth/me")
        login = client.get("/auth/login")

    assert user.json() == {"authenticated": False, "display_name": None, "email": None}
    assert login.status_code == 501


def test_frontend_fallback_is_served(tmp_path: Path) -> None:
    with TestClient(create_app(build_settings(tmp_path / "frontend.db"))) as client:
        response = client.get("/some/client/route")

    assert response.status_code == 200
    assert "SlimDash" in response.text
