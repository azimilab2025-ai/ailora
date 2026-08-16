"""Fail-closed internal composition for governed live space-data ingestion."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.config import Settings
from ailora.services.space_data.adapter import CelesTrakProviderAdapter, HttpxProviderTransport
from ailora.services.space_data.config import ProviderConfig
from ailora.services.space_data.governance import QualificationGate
from ailora.services.space_data.interfaces import (
    ProviderError,
    ProviderRequest,
    ProviderResponse,
    SpaceDataProvider,
)
from ailora.services.space_data.resilience import CircuitBreaker, RetryExecutor, RetryPolicy
from ailora.services.space_data.service import ProviderIngestionService


class ResilientSpaceDataProvider:
    """Apply bounded retry and circuit protection around a provider boundary."""

    def __init__(
        self,
        provider: SpaceDataProvider,
        retry_executor: RetryExecutor,
        circuit_breaker: CircuitBreaker,
        clock: Callable[[], datetime],
    ) -> None:
        self._provider = provider
        self._retry_executor = retry_executor
        self._circuit_breaker = circuit_breaker
        self._clock = clock

    async def fetch(self, request: ProviderRequest) -> ProviderResponse:
        self._circuit_breaker.before_call(self._clock())

        async def operation(attempt: int) -> ProviderResponse:
            del attempt
            return await self._provider.fetch(request)

        try:
            result = await self._retry_executor.run(operation)
        except ProviderError:
            self._circuit_breaker.record_failure(self._clock())
            raise
        self._circuit_breaker.record_success()
        return result


def build_live_provider_ingestion_service(
    *,
    session: AsyncSession,
    settings: Settings,
    clock: Callable[[], datetime],
    sleeper: Callable[[float], Awaitable[None]],
    transport: httpx.AsyncBaseTransport | None = None,
) -> ProviderIngestionService:
    """Compose the internal live path without activating or exposing it publicly."""

    config = ProviderConfig.from_settings(settings)
    adapter = CelesTrakProviderAdapter(
        config,
        HttpxProviderTransport(transport=transport, trust_env=False),
        clock,
    )
    resilient_provider = ResilientSpaceDataProvider(
        adapter,
        RetryExecutor(RetryPolicy(), sleeper),
        CircuitBreaker(failure_threshold=3, recovery_seconds=30.0),
        clock,
    )
    return ProviderIngestionService(session, resilient_provider, QualificationGate())
