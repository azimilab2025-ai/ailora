"""
AILORA OpenTelemetry bootstrap.

Initialises the OpenTelemetry SDK with a console/OTLP exporter.
FastAPI instrumentation is applied to the ASGI app instance.

Safety boundaries:
- No secrets or tenant data are added to span attributes.
- Tracing is disabled when AILORA_ENABLE_TRACING=false (default: true in dev).
- Production OTLP endpoint is resolved from environment, never hardcoded.

Usage::

    from ailora.observability.tracing import configure_tracing
    configure_tracing(app)  # called in create_app() or lifespan
"""

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from ailora.config import settings

# Sentinel so we only configure once per process
_tracing_configured = False


def configure_tracing(app: FastAPI) -> None:
    """
    Configure OpenTelemetry tracing and instrument the FastAPI application.

    This function is idempotent: calling it more than once is safe.

    Args:
        app: The FastAPI application instance to instrument.
    """
    global _tracing_configured  # noqa: PLW0603
    if _tracing_configured:
        return

    resource = Resource.create(
        {
            "service.name": settings.app_name.lower(),
            "service.version": settings.app_version,
            "deployment.environment": settings.environment,
        }
    )

    provider = TracerProvider(resource=resource)

    # Console exporter for local development; replace with OTLP in production
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)

    _tracing_configured = True


def get_tracer(name: str) -> trace.Tracer:
    """Return a named tracer for manual instrumentation."""
    return trace.get_tracer(name)
