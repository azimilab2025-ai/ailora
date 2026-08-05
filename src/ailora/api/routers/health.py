"""
Health check router.

Provides liveness and readiness probes required by Prompt 15 §challenge_deliverables
and §deployment_contract.

These endpoints must never expose secrets, credentials, or internal error traces.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Standard health check response envelope."""

    status: str
    service: str
    version: str


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 when the service process is alive.",
)
async def liveness() -> HealthResponse:
    """Liveness probe — confirms the process is running."""
    return HealthResponse(status="ok", service="ailora", version="0.1.0")


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness probe",
    description="Returns 200 when the service is ready to accept requests.",
)
async def readiness() -> HealthResponse:
    """Readiness probe — confirms the service is ready to serve traffic."""
    # Phase 1: no DB yet; returns ok when application layer is healthy.
    # Phase 1 will add a real DB connectivity check here.
    return HealthResponse(status="ok", service="ailora", version="0.1.0")
