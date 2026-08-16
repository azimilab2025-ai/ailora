from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from urllib.parse import urlparse

import httpx

from ailora.services.space_data.config import ProviderConfig
from ailora.services.space_data.interfaces import (
    ProviderDisabledError,
    ProviderRequest,
    ProviderResponse,
    ProviderResponseError,
    ProviderTransport,
    TransportResponse,
)


class HttpxProviderTransport:
    """Bounded HTTPS transport used by live provider adapters."""

    def __init__(
        self,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        trust_env: bool = False,
    ) -> None:
        self._transport = transport
        self._trust_env = trust_env

    async def fetch(
        self,
        *,
        url: str,
        query: tuple[tuple[str, str], ...],
        timeout_seconds: float,
    ) -> TransportResponse:
        try:
            async with httpx.AsyncClient(
                follow_redirects=False,
                transport=self._transport,
                trust_env=self._trust_env,
            ) as client:
                response = await client.get(
                    url,
                    params=query,
                    timeout=timeout_seconds,
                    headers={
                        "accept": "text/plain",
                        "user-agent": "AILORA/0.1 space-data-provider",
                    },
                )
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise ProviderResponseError(
                "provider transport failure",
                retryable=True,
            ) from exc
        except httpx.RequestError as exc:
            raise ProviderResponseError(
                "provider transport request failure",
                retryable=False,
            ) from exc

        canonical_final = response.url.copy_with(query=None, fragment=None)
        return TransportResponse(
            status_code=response.status_code,
            content_type=response.headers.get("content-type", ""),
            payload=bytes(response.content),
            final_url=str(canonical_final),
            headers=tuple(response.headers.multi_items()),
        )


class CelesTrakProviderAdapter:
    def __init__(
        self,
        config: ProviderConfig,
        transport: ProviderTransport,
        clock: Callable[[], datetime],
    ) -> None:
        self._config = config
        self._transport = transport
        self._clock = clock

    async def fetch(self, request: ProviderRequest) -> ProviderResponse:
        if not self._config.enabled:
            raise ProviderDisabledError()
        url = f"{self._config.base_url}/NORAD/elements/gp.php"
        response = await self._transport.fetch(
            url=url,
            query=(("CATNR", request.object_id), ("FORMAT", "TLE")),
            timeout_seconds=self._config.timeout_seconds,
        )
        parsed_final = urlparse(response.final_url)
        if parsed_final.scheme != "https" or parsed_final.hostname != self._config.allowed_host:
            raise ProviderResponseError("redirect target is not allowlisted")
        if response.final_url != url:
            raise ProviderResponseError("redirect is forbidden")
        if response.status_code != 200:
            raise ProviderResponseError(
                f"provider status {response.status_code}",
                retryable=response.status_code >= 500,
            )
        content_type = response.content_type.split(";", maxsplit=1)[0].strip().lower()
        if content_type not in self._config.allowed_content_types:
            raise ProviderResponseError("content type is not allowed")
        if not response.payload:
            raise ProviderResponseError("empty provider response")
        if len(response.payload) > self._config.max_response_bytes:
            raise ProviderResponseError("provider response exceeds size limit")
        fetched_at = self._clock()
        if fetched_at.tzinfo is None or fetched_at.utcoffset() is None:
            raise ValueError("clock must return a timezone-aware datetime")
        return ProviderResponse(
            provider_id=self._config.provider_id,
            provider_version=self._config.provider_version,
            request_id=uuid.UUID(str(request.request_id)),
            object_id=request.object_id,
            fetched_at=fetched_at.astimezone(UTC),
            status_code=response.status_code,
            content_type=content_type,
            payload=bytes(response.payload),
            attribution_text=self._config.attribution_text,
        )
