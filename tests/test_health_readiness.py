"""Focused contracts for bounded database readiness behavior."""

import asyncio

import pytest

from ailora.api.routers import health as health_router


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
    def __init__(
        self,
        connection: _FakeConnection,
        *,
        dispose_fails: bool = False,
    ) -> None:
        self._connection = connection
        self._dispose_fails = dispose_fails
        self.disposed = False

    def connect(self) -> _FakeConnection:
        return self._connection

    async def dispose(self) -> None:
        self.disposed = True
        if self._dispose_fails:
            raise RuntimeError("private disposal detail")


def _install_engine(
    monkeypatch: pytest.MonkeyPatch,
    engine: _FakeEngine,
) -> None:
    def factory(*args: object, **kwargs: object) -> _FakeEngine:
        del args, kwargs
        return engine

    monkeypatch.setattr(health_router, "create_async_engine", factory)


@pytest.mark.asyncio
async def test_probe_disposes_engine_after_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection())
    _install_engine(monkeypatch, engine)

    assert await health_router._probe_database() is True
    assert engine.disposed is True


@pytest.mark.asyncio
async def test_probe_disposes_engine_after_connection_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection(fail=True))
    _install_engine(monkeypatch, engine)

    assert await health_router._probe_database() is False
    assert engine.disposed is True


@pytest.mark.asyncio
async def test_probe_disposes_engine_after_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection(delay=0.05))
    _install_engine(monkeypatch, engine)
    monkeypatch.setattr(health_router, "_DB_PROBE_TIMEOUT_SECONDS", 0.001)

    assert await health_router._probe_database() is False
    assert engine.disposed is True


@pytest.mark.asyncio
async def test_probe_handles_invalid_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_creation(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise ValueError("invalid database configuration")

    monkeypatch.setattr(health_router, "create_async_engine", fail_creation)

    assert await health_router._probe_database() is False


@pytest.mark.asyncio
async def test_probe_contains_disposal_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _FakeEngine(_FakeConnection(), dispose_fails=True)
    _install_engine(monkeypatch, engine)

    assert await health_router._probe_database() is False
    assert engine.disposed is True
