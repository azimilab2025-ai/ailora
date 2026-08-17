"""AILORA FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from ailora.api.contracts import (
    APIContractError,
    APIContractMiddleware,
    RequestBudget,
    api_contract_error_handler,
    http_exception_handler,
    validation_error_handler,
)
from ailora.api.routers import (
    authorization,
    health,
    identity_sessions,
    space_data,
    ssa_audit,
    ssa_reviews,
    ssa_risk_assessments,
    ssa_scenarios,
    ssa_screenings,
    tenant_identity,
)
from ailora.config import settings
from ailora.db import session as database
from ailora.observability.logging import configure_logging

configure_logging()


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Capture startup dependency state and release the shared engine on shutdown."""
    application.state.database_ready_at_startup = await database.probe_database()

    try:
        yield
    finally:
        await database.close_database()


app = FastAPI(
    title=settings.app_name,
    description="An Azimi Innovation Lab Orbital Intelligence System",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    APIContractMiddleware,
    budget=RequestBudget(
        max_body_bytes=settings.api_max_body_bytes,
        timeout_seconds=settings.api_request_timeout_seconds,
        max_page_size=settings.api_max_page_size,
    ),
)
app.add_exception_handler(APIContractError, api_contract_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

app.include_router(health.router)
app.include_router(authorization.router)
app.include_router(identity_sessions.router)
app.include_router(tenant_identity.router)
app.include_router(space_data.router)
app.include_router(ssa_scenarios.router)
app.include_router(ssa_screenings.router)
app.include_router(ssa_risk_assessments.router)
app.include_router(ssa_reviews.router)
app.include_router(ssa_audit.router)
