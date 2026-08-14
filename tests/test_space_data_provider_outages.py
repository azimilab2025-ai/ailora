from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.space_data.interfaces import ProviderError, ProviderErrorCode
from ailora.services.space_data.resilience import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
    RetryExecutor,
    RetryPolicy,
)

NOW = datetime(2026, 8, 14, 20, 0, tzinfo=UTC)


@pytest.mark.asyncio
async def test_retry_recovers_transient_failure_with_bounded_attempts() -> None:
    attempts: list[int] = []
    delays: list[float] = []

    async def operation(attempt: int) -> str:
        attempts.append(attempt)
        if attempt < 3:
            raise ProviderError(ProviderErrorCode.TIMEOUT, "timeout", retryable=True)
        return "ok"

    async def sleeper(delay: float) -> None:
        delays.append(delay)

    executor = RetryExecutor(RetryPolicy(max_attempts=3, base_delay_seconds=0.1), sleeper)
    assert await executor.run(operation) == "ok"
    assert attempts == [1, 2, 3]
    assert delays == [0.1, 0.2]


@pytest.mark.asyncio
async def test_permanent_failure_is_not_retried() -> None:
    calls = 0

    async def operation(attempt: int) -> str:
        nonlocal calls
        calls += 1
        raise ProviderError(ProviderErrorCode.AUTH, "denied", retryable=False)

    async def sleeper(delay: float) -> None:
        raise AssertionError(f"unexpected sleep: {delay}")

    with pytest.raises(ProviderError):
        await RetryExecutor(RetryPolicy(), sleeper).run(operation)
    assert calls == 1


def test_circuit_breaker_opens_and_half_opens_deterministically() -> None:
    breaker = CircuitBreaker(failure_threshold=2, recovery_seconds=30.0)
    breaker.before_call(NOW)
    breaker.record_failure(NOW)
    breaker.record_failure(NOW)
    assert breaker.state is CircuitState.OPEN
    with pytest.raises(CircuitOpenError):
        breaker.before_call(NOW + timedelta(seconds=29))
    breaker.before_call(NOW + timedelta(seconds=30))
    assert breaker.state is CircuitState.HALF_OPEN
    breaker.record_success()
    assert breaker.state is CircuitState.CLOSED
