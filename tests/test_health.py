"""HTTP contracts for liveness and fail-closed readiness."""

from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from ailora.api.app import app
from ailora.api.routers import health as health_router


@pytest.mark.asyncio
async def test_liveness_returns_ok_without_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    probe = AsyncMock(side_effect=AssertionError("liveness touched database"))
    monkeypatch.setattr(health_router, "probe_database", probe)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ailora",
        "version": "0.1.0",
    }
    probe.assert_not_awaited()


@pytest.mark.asyncio
async def test_readiness_returns_200_when_database_is_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        health_router,
        "probe_database",
        AsyncMock(return_value=True),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_readiness_returns_503_without_leaking_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        health_router,
        "probe_database",
        AsyncMock(return_value=False),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "service": "ailora",
        "version": "0.1.0",
    }

    body = response.text.casefold()
    assert "postgresql" not in body
    assert "password" not in body
    assert "traceback" not in body
    assert "private" not in body
