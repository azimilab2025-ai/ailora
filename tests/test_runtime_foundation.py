"""Production configuration and application lifecycle safety contracts."""

from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from ailora import config as config_module
from ailora.api import app as app_module
from ailora.api.app import app
from ailora.config import Settings
from ailora.db import session as database

_STRONG_TEST_SECRET = "0123456789abcdef0123456789abcdef0123456789abcdef"


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "_env_file": None,
        "environment": "local",
        "secret_key": "CHANGE_ME_BEFORE_ANY_NON_LOCAL_USE",
        "allowed_origins": ["http://localhost:3000"],
    }
    values.update(overrides)
    return Settings(**values)


def test_environment_is_typed() -> None:
    settings = _settings(environment="integration")
    environment_type = getattr(config_module, "Environment", None)

    assert environment_type is not None
    assert settings.environment is environment_type.INTEGRATION


def test_unknown_environment_is_rejected() -> None:
    with pytest.raises(ValidationError):
        _settings(environment="unknown")


@pytest.mark.parametrize("environment", ["staging", "production"])
def test_deployed_environment_rejects_placeholder_secret(
    environment: str,
) -> None:
    with pytest.raises(ValidationError, match="non-placeholder secret"):
        _settings(
            environment=environment,
            allowed_origins=[],
        )


def test_production_rejects_debug_mode() -> None:
    with pytest.raises(ValidationError, match="debug mode"):
        _settings(
            environment="production",
            secret_key=_STRONG_TEST_SECRET,
            allowed_origins=[],
            debug=True,
        )


def test_production_rejects_insecure_cors() -> None:
    with pytest.raises(ValidationError, match="must use HTTPS"):
        _settings(
            environment="production",
            secret_key=_STRONG_TEST_SECRET,
            allowed_origins=["http://example.test"],
        )


def test_production_accepts_strong_fail_closed_configuration() -> None:
    settings = _settings(
        environment="production",
        secret_key=_STRONG_TEST_SECRET,
        allowed_origins=["https://app.example.test"],
    )
    environment_type = getattr(config_module, "Environment", None)

    assert environment_type is not None
    assert settings.environment is environment_type.PRODUCTION
    assert settings.debug is False


@pytest.mark.parametrize(
    "origins",
    [
        ["*"],
        [""],
        ["https://example.test/path"],
        ["https://example.test", "https://example.test"],
    ],
)
def test_ambiguous_cors_origins_are_rejected(origins: list[str]) -> None:
    with pytest.raises(ValidationError):
        _settings(allowed_origins=origins)


@pytest.mark.asyncio
async def test_lifespan_records_startup_state_and_closes_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    probe = AsyncMock(return_value=False)
    close = AsyncMock()
    lifespan = getattr(app_module, "lifespan", None)

    monkeypatch.setattr(database, "probe_database", probe)
    monkeypatch.setattr(database, "close_database", close)

    assert lifespan is not None
    async with lifespan(app):
        assert app.state.database_ready_at_startup is False

    probe.assert_awaited_once()
    close.assert_awaited_once()


def test_live_space_data_provider_is_disabled_by_default() -> None:
    from ailora.config import Settings

    runtime = Settings(_env_file=None)
    assert runtime.enable_live_space_data_provider is False
    assert runtime.celestrak_base_url == "https://celestrak.org"


@pytest.mark.parametrize(
    "unsafe_url",
    [
        "http://celestrak.org",
        "https://evil.example",
        "https://user@celestrak.org",
        "https://celestrak.org:8443",
        "https://celestrak.org/path",
    ],
)
def test_runtime_rejects_noncanonical_celestrak_origin(
    monkeypatch: pytest.MonkeyPatch,
    unsafe_url: str,
) -> None:
    from ailora.config import Settings

    monkeypatch.setenv("AILORA_CELESTRAK_BASE_URL", unsafe_url)
    with pytest.raises(ValueError, match="CelesTrak"):
        Settings(_env_file=None)
