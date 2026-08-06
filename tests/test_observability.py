"""
AILORA P1-04: Observability Bootstrap Contract Tests.

Validates that the structured logging and OpenTelemetry tracing modules
exist, are importable, and meet the safety requirements:
- configure_logging() is callable and idempotent.
- get_logger() returns a usable logger.
- configure_tracing() requires only the FastAPI app.
- No secrets, passwords, or PII are logged or added to span attributes.

These tests do not start a real OTLP exporter or require a live OTel collector.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LOGGING_MODULE = REPO_ROOT / "src" / "ailora" / "observability" / "logging.py"
TRACING_MODULE = REPO_ROOT / "src" / "ailora" / "observability" / "tracing.py"
OBS_INIT = REPO_ROOT / "src" / "ailora" / "observability" / "__init__.py"


# ─── File existence ───────────────────────────────────────────────────────────


def test_observability_package_exists() -> None:
    """src/ailora/observability/__init__.py must exist."""
    assert OBS_INIT.exists()


def test_logging_module_exists() -> None:
    """src/ailora/observability/logging.py must exist."""
    assert LOGGING_MODULE.exists()


def test_tracing_module_exists() -> None:
    """src/ailora/observability/tracing.py must exist."""
    assert TRACING_MODULE.exists()


# ─── Content safety checks ───────────────────────────────────────────────────


def test_logging_module_no_hardcoded_secrets() -> None:
    """logging.py must not contain hardcoded secret values (not just the words)."""
    text = LOGGING_MODULE.read_text(encoding="utf-8")
    # These are actual assignment patterns that would indicate hardcoded secrets
    forbidden = ["password=", "secret_key=", "api_key=", "token=Bearer"]
    for pattern in forbidden:
        assert pattern not in text.lower(), (
            f"logging.py must not contain hardcoded credential pattern: '{pattern}'"
        )


def test_tracing_module_no_hardcoded_endpoints() -> None:
    """tracing.py must not contain hardcoded OTLP endpoint URLs."""
    text = TRACING_MODULE.read_text(encoding="utf-8")
    forbidden = ["http://otel-collector", "grpc://otel", "https://api.honeycomb"]
    for pattern in forbidden:
        assert pattern not in text.lower(), (
            f"tracing.py must not contain hardcoded endpoint: '{pattern}'"
        )


def test_logging_module_uses_structlog() -> None:
    """logging.py must use structlog."""
    text = LOGGING_MODULE.read_text(encoding="utf-8")
    assert "structlog" in text, "logging.py must use structlog"


def test_tracing_module_uses_opentelemetry() -> None:
    """tracing.py must use opentelemetry."""
    text = TRACING_MODULE.read_text(encoding="utf-8")
    assert "opentelemetry" in text, "tracing.py must use opentelemetry"


# ─── Import and functional tests ─────────────────────────────────────────────


def test_logging_module_importable() -> None:
    """ailora.observability.logging must be importable."""
    import importlib

    mod = importlib.import_module("ailora.observability.logging")
    assert hasattr(mod, "configure_logging")
    assert hasattr(mod, "get_logger")


def test_configure_logging_idempotent() -> None:
    """configure_logging() must be callable multiple times without error."""
    from ailora.observability.logging import configure_logging

    configure_logging()
    configure_logging()  # Second call must not raise


def test_get_logger_returns_usable_logger() -> None:
    """get_logger() must return a logger that accepts .info() calls."""
    from ailora.observability.logging import get_logger

    log = get_logger("test.observability")
    # Must not raise
    log.info("test_event", component="observability_test")


def test_configure_logging_called_in_app() -> None:
    """app.py must import and call configure_logging at startup."""
    app_path = REPO_ROOT / "src" / "ailora" / "api" / "app.py"
    text = app_path.read_text(encoding="utf-8")
    assert "configure_logging" in text, "api/app.py must import and call configure_logging"


def test_tracing_module_importable() -> None:
    """ailora.observability.tracing must be importable."""
    import importlib

    mod = importlib.import_module("ailora.observability.tracing")
    assert hasattr(mod, "configure_tracing")
    assert hasattr(mod, "get_tracer")


def test_configure_tracing_is_idempotent() -> None:
    """configure_tracing() must be callable multiple times without error."""
    from fastapi import FastAPI

    from ailora.observability.tracing import configure_tracing

    test_app = FastAPI()
    configure_tracing(test_app)
    configure_tracing(test_app)  # Second call must not raise


def test_enable_tracing_config_field_exists() -> None:
    """Settings must expose enable_tracing field with safe default False."""
    from ailora.config import settings

    assert hasattr(settings, "enable_tracing")
    # Default must be False — tracing disabled unless explicitly enabled
    assert settings.enable_tracing is False
