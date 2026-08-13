"""AILORA FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ailora.api.routers import authorization, health, identity_sessions
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

app.include_router(health.router)
app.include_router(authorization.router)
app.include_router(identity_sessions.router)
