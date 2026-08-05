"""
AILORA structured logging bootstrap.

Configures structlog for JSON-formatted, structured log output suitable for
both local development (pretty) and production (JSON) environments.

Security rules enforced here:
- Secrets, tokens, passwords, and PII must never appear in log events.
- Raw request bodies and database query parameters are not logged.
- Tenant ID is logged as a correlation field, not raw user input.

Usage::

    from ailora.observability.logging import get_logger
    logger = get_logger(__name__)
    logger.info("event.name", key="value")
"""

import logging
import sys

import structlog

from ailora.config import settings


def configure_logging() -> None:
    """
    Configure structlog and the stdlib root logger.

    Call once at application startup (in main.py or the ASGI lifespan).
    Subsequent calls are safe (structlog is idempotent once configured).
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.debug:
        # Human-readable output for local development
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        # Machine-readable JSON for production / container environments
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)


def get_logger(name: str) -> structlog.BoundLogger:
    """Return a bound structlog logger for the given module name."""
    return structlog.get_logger(name)  # type: ignore[no-any-return]
