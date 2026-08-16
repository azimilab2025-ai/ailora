"""
AILORA Oya Voice AI — Contract Tests.

Validates:
- ENABLE_OYA_VOICE_SERVICE defaults to False (safe default).
- OyaSettings.is_active is False without production credentials.
- Fail-closed: enable_oya_voice_service=True without api_key is reset to False.
- NoOpOyaAdapter.is_active() always returns False in production-grade mode.
- start_session() never makes network calls (no-op returns DEGRADED state).
- health_check() returns safe status without sensitive data.
- Default adapter is the no-op implementation.
- No network imports or calls in production-grade adapter.
- Advisory flag is always True on session results.
"""

from __future__ import annotations

import pytest

from ailora.services.oya.adapter import NoOpOyaAdapter, default_oya_adapter
from ailora.services.oya.config import OyaSettings
from ailora.services.oya.interfaces import (
    OyaFallbackMode,
    OyaSessionConfig,
    OyaSessionState,
    OyaVoiceAdapter,
)

# ─── Default configuration (production-grade phase) ─────────────────────────────────


def test_oya_disabled_by_default() -> None:
    """ENABLE_OYA_VOICE_SERVICE must default to False."""
    s = OyaSettings()
    assert s.enable_oya_voice_service is False


def test_oya_is_active_false_without_credentials() -> None:
    """is_active must be False when api_key is empty."""
    s = OyaSettings()
    assert s.is_active is False


def test_oya_fail_closed_flag_true_no_credentials() -> None:
    """Enabling the flag without credentials must be reset to False (fail-closed)."""
    s = OyaSettings(
        enable_oya_voice_service=True,
        oya_api_key="",  # no key
        oya_environment="production-grade",
    )
    assert s.enable_oya_voice_service is False
    assert s.is_active is False


def test_oya_fail_closed_flag_true_wrong_environment() -> None:
    """Production key + non-production environment must remain disabled."""
    s = OyaSettings(
        enable_oya_voice_service=True,
        oya_api_key="some-real-key",
        oya_environment="staging",  # not "production"
    )
    assert s.enable_oya_voice_service is False
    assert s.is_active is False


def test_oya_api_key_field_exists() -> None:
    """OyaSettings must expose oya_api_key placeholder."""
    s = OyaSettings()
    assert hasattr(s, "oya_api_key")
    assert s.oya_api_key == ""


def test_oya_base_url_placeholder_exists() -> None:
    s = OyaSettings()
    assert hasattr(s, "oya_base_url")


def test_oya_webhook_secret_placeholder_exists() -> None:
    s = OyaSettings()
    assert hasattr(s, "oya_webhook_secret")


# ─── No-op adapter ────────────────────────────────────────────────────────────


def test_noop_adapter_is_not_active() -> None:
    adapter = NoOpOyaAdapter()
    assert adapter.is_active() is False


def test_noop_adapter_is_oya_voice_adapter() -> None:
    assert isinstance(NoOpOyaAdapter(), OyaVoiceAdapter)


@pytest.mark.asyncio
async def test_noop_adapter_start_session_returns_degraded() -> None:
    adapter = NoOpOyaAdapter()
    config = OyaSessionConfig(tenant_id="t1", user_id="u1")
    result = await adapter.start_session(config)
    assert result.state == OyaSessionState.DEGRADED
    assert result.fallback_applied is True


@pytest.mark.asyncio
async def test_noop_adapter_start_session_is_advisory() -> None:
    adapter = NoOpOyaAdapter()
    config = OyaSessionConfig(tenant_id="t1", user_id="u1")
    result = await adapter.start_session(config)
    assert result.is_advisory is True


@pytest.mark.asyncio
async def test_noop_adapter_start_session_no_network_call() -> None:
    """start_session must complete without any network call."""
    import asyncio

    adapter = NoOpOyaAdapter()
    config = OyaSessionConfig(tenant_id="t1", user_id="u1")
    # Must complete almost instantly — no real network IO
    result = await asyncio.wait_for(adapter.start_session(config), timeout=1.0)
    assert result is not None


@pytest.mark.asyncio
async def test_noop_adapter_end_session_no_error() -> None:
    adapter = NoOpOyaAdapter()
    # Must not raise
    await adapter.end_session("session-123")


@pytest.mark.asyncio
async def test_noop_adapter_health_check_returns_disabled() -> None:
    adapter = NoOpOyaAdapter()
    health = await adapter.health_check()
    assert health["is_active"] is False
    assert health["status"] == "disabled"


@pytest.mark.asyncio
async def test_noop_adapter_health_no_secrets() -> None:
    """Health check must not expose secrets."""
    adapter = NoOpOyaAdapter()
    health = await adapter.health_check()
    health_str = str(health).lower()
    assert "api_key" not in health_str
    assert "secret" not in health_str
    assert "password" not in health_str


def test_default_adapter_is_noop() -> None:
    """The default_oya_adapter must be the no-op implementation."""
    assert isinstance(default_oya_adapter, NoOpOyaAdapter)


def test_default_adapter_not_active() -> None:
    assert default_oya_adapter.is_active() is False


# ─── Fallback to text chat ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_noop_adapter_fallback_mode_is_text_chat() -> None:
    adapter = NoOpOyaAdapter()
    config = OyaSessionConfig(
        tenant_id="t1",
        user_id="u1",
        fallback_mode=OyaFallbackMode.TEXT_CHAT,
    )
    result = await adapter.start_session(config)
    assert result.fallback_applied is True
    assert result.state == OyaSessionState.DEGRADED


# ─── Module boundary ─────────────────────────────────────────────────────────


def test_adapter_module_no_network_imports() -> None:
    """Adapter module must not import requests, httpx, or similar in production-grade."""
    from pathlib import Path

    text = (
        (Path(__file__).parent.parent / "src" / "ailora" / "services" / "oya" / "adapter.py")
        .read_text()
        .lower()
    )
    forbidden = ["import requests", "import httpx", "import aiohttp"]
    for f in forbidden:
        assert f not in text, f"adapter.py must not import network library: '{f}'"


def test_env_example_has_oya_placeholders() -> None:
    """`.env.example` must document Oya configuration placeholders."""
    from pathlib import Path

    text = (Path(__file__).parent.parent / ".env.example").read_text(encoding="utf-8")
    assert "OYA_VOICE_SERVICE" in text
    assert "OYA_API_KEY" in text
    assert "OYA_BASE_URL" in text
    assert "OYA_WEBHOOK_SECRET" in text


def test_env_example_oya_disabled_by_default() -> None:
    """`.env.example` must set ENABLE_OYA_VOICE_SERVICE=false."""
    from pathlib import Path

    text = (Path(__file__).parent.parent / ".env.example").read_text(encoding="utf-8")
    assert "ENABLE_OYA_VOICE_SERVICE=false" in text
