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
async def test_readiness_returns_200_with_safe_status() -> None:
    """
    GET /health/ready must always return HTTP 200.

    The response status field is 'ok' when DB is reachable, 'not_ready' when
    the DB probe fails — both are valid, deterministic, safe responses.
    The endpoint must never raise, crash, or leak internals regardless of DB state.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    # Contract: status is always one of the two known safe values
    assert data["status"] in {"ok", "not_ready"}
    assert data["service"] == "ailora"
    assert "version" in data
    # Contract: no internals, secrets, or DB details in response
    body_str = response.text
    assert "postgresql" not in body_str.lower()
    assert "password" not in body_str.lower()
    assert "traceback" not in body_str.lower()
