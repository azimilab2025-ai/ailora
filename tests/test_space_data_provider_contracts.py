from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from ailora.services.space_data.adapter import CelesTrakProviderAdapter
from ailora.services.space_data.config import ProviderConfig
from ailora.services.space_data.interfaces import (
    ProviderDisabledError,
    ProviderRequest,
    ProviderResponseError,
    TransportResponse,
)

NOW = datetime(2026, 8, 14, 20, 0, tzinfo=UTC)


class FakeTransport:
    def __init__(self, response: TransportResponse) -> None:
        self.response = response
        self.calls = 0

    async def fetch(
        self,
        *,
        url: str,
        query: tuple[tuple[str, str], ...],
        timeout_seconds: float,
    ) -> TransportResponse:
        del url, query, timeout_seconds
        self.calls += 1
        return self.response


def request() -> ProviderRequest:
    return ProviderRequest(
        request_id=uuid.uuid4(),
        object_id="25544",
        evaluated_at=NOW,
        purpose="advisory conjunction screening",
    )


def response(
    *,
    status_code: int = 200,
    content_type: str = "text/plain",
    payload: bytes = b"ISS\n1 00000U TEST\n2 00000 TEST\n",
    final_url: str = "https://celestrak.org/NORAD/elements/gp.php",
    headers: tuple[tuple[str, str], ...] = (),
) -> TransportResponse:
    return TransportResponse(
        status_code=status_code,
        content_type=content_type,
        payload=payload,
        final_url=final_url,
        headers=headers,
    )


def test_provider_config_is_disabled_by_default() -> None:
    assert ProviderConfig().enabled is False


@pytest.mark.parametrize(
    "base_url",
    [
        "http://celestrak.org",
        "https://user@celestrak.org",
        "https://celestrak.org:8443",
        "https://celestrak.org/path",
    ],
)
def test_provider_config_rejects_noncanonical_origin(base_url: str) -> None:
    with pytest.raises(ValueError):
        ProviderConfig(base_url=base_url)


@pytest.mark.asyncio
async def test_disabled_adapter_never_calls_transport() -> None:
    transport = FakeTransport(response())
    adapter = CelesTrakProviderAdapter(ProviderConfig(), transport, lambda: NOW)
    with pytest.raises(ProviderDisabledError):
        await adapter.fetch(request())
    assert transport.calls == 0


@pytest.mark.asyncio
async def test_enabled_adapter_returns_bounded_response() -> None:
    transport = FakeTransport(response())
    config = ProviderConfig(enabled=True)
    result = await CelesTrakProviderAdapter(config, transport, lambda: NOW).fetch(request())
    assert result.payload.startswith(b"ISS")
    assert result.provider_id == "CELESTRAK"
    assert transport.calls == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"status_code": 500}, "status"),
        ({"content_type": "text/html"}, "content type"),
        ({"final_url": "https://evil.example/data"}, "redirect"),
        ({"payload": b""}, "empty"),
        ({"payload": b"x" * 131_073}, "size limit"),
    ],
)
async def test_adapter_rejects_invalid_responses(override: dict[str, object], message: str) -> None:
    transport = FakeTransport(response(**override))
    adapter = CelesTrakProviderAdapter(ProviderConfig(enabled=True), transport, lambda: NOW)
    with pytest.raises(ProviderResponseError, match=message):
        await adapter.fetch(request())


def test_request_rejects_naive_time_and_unsafe_identity() -> None:
    with pytest.raises(ValueError):
        ProviderRequest(uuid.uuid4(), "25544", datetime(2026, 1, 1), "safe")
    with pytest.raises(ValueError):
        ProviderRequest(uuid.uuid4(), "../25544", NOW, "safe")
