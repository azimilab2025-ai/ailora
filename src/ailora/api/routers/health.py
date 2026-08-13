"""Bounded health endpoints that never expose database internals."""

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from ailora.config import settings
from ailora.db.session import probe_database

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Standard bounded health response."""

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
    """Confirm process liveness without touching external dependencies."""
    return HealthResponse(
        status="ok",
        service="ailora",
        version=settings.app_version,
    )


@router.get(
    "/ready",
    response_model=HealthResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "A required dependency is unavailable.",
            "model": HealthResponse,
        }
    },
    summary="Readiness probe",
    description=(
        "Returns 200 when required dependencies are ready and 503 otherwise. "
        "No connection details or internal failures are exposed."
    ),
)
async def readiness(response: Response) -> HealthResponse:
    """Fail closed with HTTP 503 when the shared database probe fails."""
    if await probe_database():
        return HealthResponse(
            status="ok",
            service="ailora",
            version=settings.app_version,
        )

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(
        status="not_ready",
        service="ailora",
        version=settings.app_version,
    )
