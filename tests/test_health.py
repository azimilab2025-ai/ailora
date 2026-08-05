"""
Tests for the AILORA health check endpoints.

Validates both liveness and readiness probes return 200 with correct payload.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from ailora.api.app import app


@pytest.mark.asyncio
async def test_liveness_returns_ok() -> None:
    """GET /health/live must return 200 with status=ok."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ailora"
    assert "version" in data


@pytest.mark.asyncio
async def test_readiness_returns_ok() -> None:
    """GET /health/ready must return 200 with status=ok."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ailora"
