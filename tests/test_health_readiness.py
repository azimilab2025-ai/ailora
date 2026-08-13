"""Focused contracts for the shared database lifecycle and readiness recovery."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from ailora.api.app import app
from ailora.api.routers import health as health_router
from ailora.db import session as database


class _FakeConnection:
    def __init__(self, *, fail: bool = False, delay: float = 0.0) -> None:
        self._fail = fail
        self._delay = delay

    async def __aenter__(self) -> "_FakeConnection":
        if self._fail:
            raise RuntimeError("private database detail")
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc: object,
        traceback: object,
    ) -> None:
        del exc_type, exc, traceback

    async def execute(self, statement: object) -> None:
        del statement
        if self._delay:
            await asyncio.sleep(self._delay)


class _FakeEngine:
    def __init__(self, connection: _FakeConnection) -> None:
        self._connection = connection
        self.connect_count = 0
        self.dispose_count = 0

    def connect(self) -> _FakeConnection:
        self.connect_count += 1
        return self._connection

    async def dispose(self) -> None:
        self.dispose_count += 1


@pytest.mark.asyncio
async def test_shared_engine_is_reused_for_multiple_probes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection())
    monkeypatch.setattr(database, "engine", engine)

    assert await database.probe_database() is True
    assert await database.probe_database() is True
    assert engine.connect_count == 2
    assert engine.dispose_count == 0


@pytest.mark.asyncio
async def test_probe_contains_connection_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection(fail=True))
    monkeypatch.setattr(database, "engine", engine)

    assert await database.probe_database() is False


@pytest.mark.asyncio
async def test_probe_contains_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection(delay=0.05))
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(
        database.settings,
        "database_probe_timeout_seconds",
        0.001,
    )

    assert await database.probe_database() is False


@pytest.mark.asyncio
async def test_readiness_recovers_after_dependency_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    probe = AsyncMock(side_effect=[False, True])
    monkeypatch.setattr(health_router, "probe_database", probe)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        unavailable = await client.get("/health/ready")
        recovered = await client.get("/health/ready")

    assert unavailable.status_code == 503
    assert unavailable.json()["status"] == "not_ready"
    assert recovered.status_code == 200
    assert recovered.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_shutdown_disposes_shared_engine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection())
    monkeypatch.setattr(database, "engine", engine)

    await database.close_database()

    assert engine.dispose_count == 1
