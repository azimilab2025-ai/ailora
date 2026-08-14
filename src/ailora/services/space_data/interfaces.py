from __future__ import annotations

import re
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol

_OBJECT_ID = re.compile(r"^[A-Z0-9._:-]{1,128}$")


class ProviderErrorCode(StrEnum):
    DISABLED = "DISABLED"
    UNQUALIFIED = "UNQUALIFIED"
    AUTH = "AUTH"
    RATE_LIMIT = "RATE_LIMIT"
    TIMEOUT = "TIMEOUT"
    OUTAGE = "OUTAGE"
    INVALID_RESPONSE = "INVALID_RESPONSE"


class ProviderError(RuntimeError):
    def __init__(self, code: ProviderErrorCode, detail: str, *, retryable: bool) -> None:
        super().__init__(detail)
        self.code = code
        self.retryable = retryable


class ProviderDisabledError(ProviderError):
    def __init__(self) -> None:
        super().__init__(ProviderErrorCode.DISABLED, "provider is disabled", retryable=False)


class ProviderResponseError(ProviderError):
    def __init__(self, detail: str, *, retryable: bool = False) -> None:
        super().__init__(ProviderErrorCode.INVALID_RESPONSE, detail, retryable=retryable)


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    request_id: uuid.UUID
    object_id: str
    evaluated_at: datetime
    purpose: str

    def __post_init__(self) -> None:
        if not _OBJECT_ID.fullmatch(self.object_id.upper()):
            raise ValueError("object_id is invalid")
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() is None:
            raise ValueError("evaluated_at must be timezone-aware")
        if not self.purpose.strip() or len(self.purpose) > 256:
            raise ValueError("purpose is invalid")
        object.__setattr__(self, "object_id", self.object_id.upper())
        object.__setattr__(self, "evaluated_at", self.evaluated_at.astimezone(UTC))


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status_code: int
    content_type: str
    payload: bytes
    final_url: str
    headers: tuple[tuple[str, str], ...]

    def header_map(self) -> Mapping[str, str]:
        return {key.lower(): value for key, value in self.headers}


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    provider_id: str
    provider_version: str
    request_id: uuid.UUID
    object_id: str
    fetched_at: datetime
    status_code: int
    content_type: str
    payload: bytes
    attribution_text: str


class ProviderTransport(Protocol):
    async def fetch(
        self,
        *,
        url: str,
        query: tuple[tuple[str, str], ...],
        timeout_seconds: float,
    ) -> TransportResponse: ...


class SpaceDataProvider(Protocol):
    async def fetch(self, request: ProviderRequest) -> ProviderResponse: ...
