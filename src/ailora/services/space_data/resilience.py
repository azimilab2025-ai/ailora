from __future__ import annotations

import math
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import TypeVar

from ailora.services.space_data.interfaces import ProviderError

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 2.0

    def __post_init__(self) -> None:
        if not 1 <= self.max_attempts <= 5:
            raise ValueError("max_attempts must be between one and five")
        if not 0 <= self.base_delay_seconds <= self.max_delay_seconds <= 10:
            raise ValueError("retry delay bounds are invalid")

    def delay(self, completed_attempt: int) -> float:
        if completed_attempt < 1:
            raise ValueError("completed_attempt must be positive")
        exponential_delay = self.base_delay_seconds * math.pow(2.0, completed_attempt - 1)
        return min(exponential_delay, self.max_delay_seconds)


class RetryExecutor:
    def __init__(
        self,
        policy: RetryPolicy,
        sleeper: Callable[[float], Awaitable[None]],
    ) -> None:
        self._policy = policy
        self._sleeper = sleeper

    async def run(self, operation: Callable[[int], Awaitable[T]]) -> T:
        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                return await operation(attempt)
            except ProviderError as exc:
                if not exc.retryable or attempt >= self._policy.max_attempts:
                    raise
                await self._sleeper(self._policy.delay(attempt))
        raise AssertionError("retry loop exhausted unexpectedly")


class CircuitState(StrEnum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitOpenError(RuntimeError):
    pass


class CircuitBreaker:
    def __init__(self, *, failure_threshold: int, recovery_seconds: float) -> None:
        if failure_threshold < 1 or recovery_seconds <= 0:
            raise ValueError("circuit breaker configuration is invalid")
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds
        self.state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at: datetime | None = None

    def before_call(self, now: datetime) -> None:
        if self.state is CircuitState.OPEN:
            if self._opened_at is None:
                raise RuntimeError("open circuit is missing its transition timestamp")
            if now < self._opened_at + timedelta(seconds=self.recovery_seconds):
                raise CircuitOpenError("provider circuit is open")
            self.state = CircuitState.HALF_OPEN

    def record_failure(self, now: datetime) -> None:
        self._failures += 1
        if self._failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self._opened_at = now

    def record_success(self) -> None:
        self.state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at = None
