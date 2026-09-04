"""Tests for environment configuration validation."""

from unittest.mock import patch

import pytest

from slimdash.bootstrap.config import Settings


def test_loads_typed_environment_values() -> None:
    with patch.dict(
        "os.environ",
        {
            "APP_PORT": "9000",
            "APP_SECURE_COOKIES": "true",
            "APP_ALLOWED_HOSTS": "example.test, api.example.test",
        },
        clear=True,
    ):
        settings = Settings()

    assert settings.port == 9000
    assert settings.secure_cookies is True
    assert settings.allowed_hosts == ["example.test", "api.example.test"]


def test_rejects_partial_oidc_configuration() -> None:
    with patch.dict("os.environ", {"W3ID_CLIENT_ID": "client"}, clear=True):
        settings = Settings()

    with pytest.raises(ValueError, match="are a set"):
        _ = settings.oidc_enabled


def test_rejects_insecure_production_configuration() -> None:
    with patch.dict(
        "os.environ",
        {"APP_ENV": "production", "APP_SESSION_SECRET": "short"},
        clear=True,
    ):
        settings = Settings()

    with pytest.raises(ValueError, match="32 characters"):
        settings.validate_security()
