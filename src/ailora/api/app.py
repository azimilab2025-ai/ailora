"""
AILORA FastAPI application factory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ailora.api.routers import health
from ailora.config import settings
from ailora.observability.logging import configure_logging

# Configure structured logging at import time so all modules that call
# get_logger() receive a configured logger even before the ASGI server starts.
configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="An Azimi Innovation Lab Orbital Intelligence System",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
