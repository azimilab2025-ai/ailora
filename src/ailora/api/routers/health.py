"""
Health check router.

Provides liveness and readiness probes required by Prompt 15 §challenge_deliverables
and §deployment_contract.

These endpoints must never expose secrets, credentials, or internal error traces.
"""

import asyncio

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from ailora.config import settings

router = APIRouter(prefix="/health", tags=["Health"])

# Bounded timeout for DB probe — prevents readiness hanging on DB failure
_DB_PROBE_TIMEOUT_SECONDS = 3.0


class HealthResponse(BaseModel):
    """Standard health check response envelope."""

    status: str
    service: str
    version: str


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 when the service process is alive. No DB dependency.",
)
async def liveness() -> HealthResponse:
    """Liveness probe — confirms the process is running. Never touches the DB."""
    return HealthResponse(status="ok", service="ailora", version=settings.app_version)


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness probe",
    description=(
        "Returns 200 when the service is ready to accept requests. "
        "Performs a bounded read-only DB probe. "
        "Returns 200 with status='not_ready' on DB failure — never leaks internals."
    ),
)
async def readiness() -> HealthResponse:
    """
    Readiness probe — performs a bounded, read-only DB connectivity check.

    Returns status='ok' when DB is reachable, status='not_ready' otherwise.
    The HTTP response is always 200 to allow load-balancer health checks to
    distinguish a running-but-not-ready service from a crashed process.
    No secrets, credentials, connection strings, or stack traces are returned.
    """
    db_ok = await _probe_database()
    status = "ok" if db_ok else "not_ready"
    return HealthResponse(status=status, service="ailora", version=settings.app_version)


async def _probe_database() -> bool:
    """
    Execute a single lightweight read-only query against the configured database.

    Returns True if the database responded within the bounded timeout.
    Returns False on any error or timeout without raising or leaking details.
    """
    try:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        async with asyncio.timeout(_DB_PROBE_TIMEOUT_SECONDS):
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        await engine.dispose()
        return True
    except Exception:  # noqa: BLE001
        return False
