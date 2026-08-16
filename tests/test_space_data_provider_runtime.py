from __future__ import annotations

import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import httpx
import pytest

from ailora.services.space_data.interfaces import (
    ProviderError,
    ProviderErrorCode,
    ProviderRequest,
    ProviderResponse,
)
from ailora.services.space_data.resilience import (
    CircuitBreaker,
    CircuitState,
    RetryExecutor,
    RetryPolicy,
)
from ailora.services.space_data.runtime import (
    ResilientSpaceDataProvider,
    build_live_provider_ingestion_service,
)
from ailora.services.space_data.service import ProviderIngestionService

NOW = datetime(2026, 8, 17, 20, 0, tzinfo=UTC)


def request() -> ProviderRequest:
    return ProviderRequest(uuid.uuid4(), "25544", NOW, "advisory screening")


def response(value: ProviderRequest) -> ProviderResponse:
    return ProviderResponse(
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        request_id=value.request_id,
        object_id=value.object_id,
        fetched_at=NOW,
        status_code=200,
        content_type="text/plain",
        payload=b"bounded-tle",
        attribution_text="attribution required",
    )


@pytest.mark.asyncio
async def test_runtime_retries_transient_failure_and_closes_circuit() -> None:
    calls = 0
    delays: list[float] = []

    class Provider:
        async def fetch(self, value: ProviderRequest) -> ProviderResponse:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise ProviderError(ProviderErrorCode.TIMEOUT, "timeout", retryable=True)
            return response(value)

    async def sleeper(delay: float) -> None:
        delays.append(delay)

    breaker = CircuitBreaker(failure_threshold=2, recovery_seconds=30.0)
    runtime = ResilientSpaceDataProvider(
        Provider(),
        RetryExecutor(RetryPolicy(max_attempts=2, base_delay_seconds=0.1), sleeper),
        breaker,
        lambda: NOW,
    )
    result = await runtime.fetch(request())
    assert result.payload == b"bounded-tle"
    assert calls == 2
    assert delays == [0.1]
    assert breaker.state is CircuitState.CLOSED


@pytest.mark.asyncio
async def test_runtime_opens_circuit_after_bounded_terminal_failures() -> None:
    calls = 0

    class Provider:
        async def fetch(self, value: ProviderRequest) -> ProviderResponse:
            nonlocal calls
            del value
            calls += 1
            raise ProviderError(ProviderErrorCode.TIMEOUT, "timeout", retryable=True)

    async def sleeper(delay: float) -> None:
        raise AssertionError(f"unexpected sleep: {delay}")

    breaker = CircuitBreaker(failure_threshold=2, recovery_seconds=30.0)
    runtime = ResilientSpaceDataProvider(
        Provider(), RetryExecutor(RetryPolicy(max_attempts=1), sleeper), breaker, lambda: NOW
    )
    with pytest.raises(ProviderError):
        await runtime.fetch(request())
    with pytest.raises(ProviderError):
        await runtime.fetch(request())
    assert calls == 2
    assert breaker.state is CircuitState.OPEN
    with pytest.raises(RuntimeError, match="circuit"):
        await runtime.fetch(request())
    assert calls == 2


def test_factory_composes_internal_path_without_network_activity() -> None:
    network_calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        network_calls.append(str(request.url))
        raise AssertionError("factory construction must not perform network activity")

    async def sleeper(delay: float) -> None:
        raise AssertionError(f"factory construction must not sleep: {delay}")

    runtime_settings = SimpleNamespace(
        enable_live_space_data_provider=False,
        celestrak_base_url="https://celestrak.org",
        celestrak_timeout_seconds=5.0,
        celestrak_max_response_bytes=131_072,
    )
    service = build_live_provider_ingestion_service(
        session=object(),
        settings=runtime_settings,
        clock=lambda: NOW,
        sleeper=sleeper,
        transport=httpx.MockTransport(handler),
    )

    assert isinstance(service, ProviderIngestionService)
    assert network_calls == []
