"""Command 16 runtime and edge-security regression contracts."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ailora.config import Settings

ROOT = Path(__file__).resolve().parents[1]
_STRONG_SECRET = "0123456789abcdef0123456789abcdef0123456789abcdef"


def production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "_env_file": None,
        "environment": "production",
        "secret_key": _STRONG_SECRET,
        "allowed_origins": [],
        "debug": False,
        "enable_live_space_data_provider": False,
        "outbound_allowed_hosts": [],
    }
    values.update(overrides)
    return Settings(**values)


def test_runtime_edge_security_defaults_are_fail_closed() -> None:
    settings = Settings(_env_file=None)
    assert settings.runtime_read_only is True
    assert settings.security_headers_enabled is True
    assert settings.outbound_https_only is True
    assert settings.outbound_allowed_hosts == []
    assert settings.rate_limit_requests_per_minute == 120


@pytest.mark.parametrize(
    "host",
    [
        "*",
        "",
        "localhost",
        "127.0.0.1",
        "169.254.169.254",
        "::1",
        "https://celestrak.org",
        "celestrak.org:443",
        "user@celestrak.org",
        "internal.local",
    ],
)
def test_outbound_allowlist_rejects_ambiguous_or_internal_hosts(host: str) -> None:
    with pytest.raises(ValidationError, match="outbound"):
        Settings(_env_file=None, outbound_allowed_hosts=[host])


def test_outbound_allowlist_accepts_explicit_dns_hostname() -> None:
    settings = Settings(_env_file=None, outbound_allowed_hosts=["celestrak.org"])
    assert settings.outbound_allowed_hosts == ["celestrak.org"]


def test_outbound_allowlist_rejects_duplicates() -> None:
    with pytest.raises(ValidationError, match="outbound"):
        Settings(
            _env_file=None,
            outbound_allowed_hosts=["celestrak.org", "celestrak.org"],
        )


@pytest.mark.parametrize(
    ("field", "unsafe_value"),
    [
        ("runtime_read_only", False),
        ("security_headers_enabled", False),
        ("outbound_https_only", False),
    ],
)
def test_production_rejects_disabled_runtime_security_controls(
    field: str,
    unsafe_value: object,
) -> None:
    with pytest.raises(ValidationError, match="production"):
        production_settings(**{field: unsafe_value})


def test_live_provider_requires_celestrak_in_explicit_outbound_allowlist() -> None:
    with pytest.raises(ValidationError, match="CelesTrak"):
        production_settings(
            enable_live_space_data_provider=True,
            outbound_allowed_hosts=[],
        )


def test_disabled_provider_does_not_require_celestrak_egress() -> None:
    settings = production_settings(
        enable_live_space_data_provider=False,
        outbound_allowed_hosts=[],
    )
    assert settings.outbound_allowed_hosts == []


@pytest.mark.parametrize("value", [0, -1, 10001])
def test_rate_limit_is_bounded(value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, rate_limit_requests_per_minute=value)


def test_runtime_image_is_non_login_and_application_tree_is_read_only() -> None:
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "--no-create-home" in text
    assert "--shell /usr/sbin/nologin" in text
    assert "chown -R root:root /app" in text
    assert "chmod -R a-w /app" in text
    assert "USER ailora" in text


def test_render_declares_fail_closed_runtime_security_defaults() -> None:
    blueprint = yaml.safe_load((ROOT / "render.yaml").read_text(encoding="utf-8"))
    service = blueprint["services"][0]
    env = {item["key"]: item for item in service["envVars"]}

    assert env["AILORA_RUNTIME_READ_ONLY"]["value"] == "true"
    assert env["AILORA_SECURITY_HEADERS_ENABLED"]["value"] == "true"
    assert env["AILORA_OUTBOUND_HTTPS_ONLY"]["value"] == "true"
    assert env["AILORA_OUTBOUND_ALLOWED_HOSTS"]["value"] == '["celestrak.org"]'
    assert env["AILORA_RATE_LIMIT_REQUESTS_PER_MINUTE"]["value"] == "120"


def test_external_edge_enforcement_is_not_falsely_claimed() -> None:
    text = (ROOT / "render.yaml").read_text(encoding="utf-8")
    assert "COMMAND_16_EXTERNAL_EDGE_GATE_OPEN" in text
    assert "WAF" in text
    assert "egress broker" in text
    assert "secret-manager" in text
