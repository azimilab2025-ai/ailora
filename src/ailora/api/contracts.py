"""Fail-closed HTTP contracts for bounded enterprise API requests."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import re
import threading
import time
import uuid
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import NoReturn

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

CORRELATION_HEADER = "X-Correlation-ID"
IDEMPOTENCY_HEADER = "Idempotency-Key"
IF_MATCH_HEADER = "If-Match"
PROBLEM_MEDIA_TYPE = "application/problem+json"
PROBLEM_TYPE_ROOT = "https://ailora.azimi-lab.com/problems"

_SAFE_TOKEN = re.compile(r"^[A-Za-z0-9._:-]+$")
_HEX_DIGEST = re.compile(r"^[a-f0-9]{64}$")


class ProblemDetails(BaseModel):
    """RFC 9457-compatible error document with an AILORA correlation extension."""

    model_config = ConfigDict(extra="forbid")

    type: str
    title: str
    status: int = Field(ge=400, le=599)
    detail: str = Field(min_length=1, max_length=512)
    instance: str
    code: str = Field(pattern=r"^[A-Z0-9_]+$")
    correlation_id: uuid.UUID


class APIContractError(Exception):
    """Typed fail-closed error that can be rendered as Problem Details."""

    def __init__(self, *, status: int, code: str, title: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail[:512]


@dataclass(frozen=True, slots=True)
class RequestBudget:
    """Runtime bounds applied before and during every HTTP request."""

    max_body_bytes: int
    timeout_seconds: float
    max_page_size: int

    def __post_init__(self) -> None:
        if not 1 <= self.max_body_bytes <= 16_777_216:
            raise ValueError("max_body_bytes must be between 1 and 16777216")
        if not 0.05 <= self.timeout_seconds <= 120:
            raise ValueError("timeout_seconds must be between 0.05 and 120")
        if not 1 <= self.max_page_size <= 500:
            raise ValueError("max_page_size must be between 1 and 500")


def _correlation_id(request: Request) -> uuid.UUID:
    value = getattr(request.state, "correlation_id", None)
    if isinstance(value, uuid.UUID):
        return value
    correlation_id = uuid.uuid4()
    request.state.correlation_id = correlation_id
    return correlation_id


def _problem_response(
    request: Request,
    *,
    status: int,
    code: str,
    title: str,
    detail: str,
) -> JSONResponse:
    correlation_id = _correlation_id(request)
    problem = ProblemDetails(
        type=f"{PROBLEM_TYPE_ROOT}/{code.casefold().replace('_', '-')}",
        title=title,
        status=status,
        detail=detail,
        instance=request.url.path,
        code=code,
        correlation_id=correlation_id,
    )
    return JSONResponse(
        status_code=status,
        content=problem.model_dump(mode="json"),
        media_type=PROBLEM_MEDIA_TYPE,
        headers={CORRELATION_HEADER: str(correlation_id)},
    )


async def api_contract_error_handler(request: Request, error: APIContractError) -> JSONResponse:
    """Render typed contract failures without leaking implementation details."""
    return _problem_response(
        request,
        status=error.status,
        code=error.code,
        title=error.title,
        detail=error.detail,
    )


async def http_exception_handler(request: Request, error: HTTPException) -> JSONResponse:
    """Normalize FastAPI HTTP errors into a stable Problem Details envelope."""
    detail = error.detail if isinstance(error.detail, str) else "Request could not be completed"
    response = _problem_response(
        request,
        status=error.status_code,
        code=f"HTTP_{error.status_code}",
        title="HTTP request rejected",
        detail=detail,
    )
    for name, value in (error.headers or {}).items():
        response.headers[name] = value
    return response


async def validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    """Return a bounded validation failure rather than reflecting raw input."""
    _ = error
    return _problem_response(
        request,
        status=422,
        code="REQUEST_VALIDATION_FAILED",
        title="Request validation failed",
        detail="One or more request fields are invalid",
    )


class APIContractMiddleware(BaseHTTPMiddleware):
    """Attach safe correlation IDs and enforce declared request budgets."""

    def __init__(self, app: ASGIApp, *, budget: RequestBudget) -> None:
        super().__init__(app)
        self._budget = budget

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        supplied = request.headers.get(CORRELATION_HEADER)
        try:
            correlation_id = uuid.UUID(supplied) if supplied else uuid.uuid4()
        except ValueError:
            return _problem_response(
                request,
                status=400,
                code="INVALID_CORRELATION_ID",
                title="Invalid correlation identifier",
                detail=f"{CORRELATION_HEADER} must be a canonical UUID",
            )
        request.state.correlation_id = correlation_id
        request.state.request_budget = self._budget

        content_length = request.headers.get("Content-Length")
        if content_length is not None:
            try:
                declared_bytes = int(content_length)
            except ValueError:
                return _problem_response(
                    request,
                    status=400,
                    code="INVALID_CONTENT_LENGTH",
                    title="Invalid content length",
                    detail="Content-Length must be a non-negative integer",
                )
            if declared_bytes < 0:
                return _problem_response(
                    request,
                    status=400,
                    code="INVALID_CONTENT_LENGTH",
                    title="Invalid content length",
                    detail="Content-Length must be a non-negative integer",
                )
            if declared_bytes > self._budget.max_body_bytes:
                return _problem_response(
                    request,
                    status=413,
                    code="REQUEST_BODY_TOO_LARGE",
                    title="Request body exceeds budget",
                    detail="Request body is larger than the configured API budget",
                )

        try:
            async with asyncio.timeout(self._budget.timeout_seconds):
                response = await call_next(request)
        except TimeoutError:
            return _problem_response(
                request,
                status=504,
                code="REQUEST_BUDGET_EXHAUSTED",
                title="Request budget exhausted",
                detail="Request exceeded the configured processing deadline",
            )
        response.headers[CORRELATION_HEADER] = str(correlation_id)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        return response


def validate_idempotency_key(value: str | None) -> str:
    """Validate a bounded, opaque idempotency key without normalizing identity."""
    if value is None or not 16 <= len(value) <= 128 or not _SAFE_TOKEN.fullmatch(value):
        raise APIContractError(
            status=400,
            code="INVALID_IDEMPOTENCY_KEY",
            title="Invalid idempotency key",
            detail=f"{IDEMPOTENCY_HEADER} must contain 16-128 safe characters",
        )
    return value


def idempotency_fingerprint(*, method: str, path: str, tenant_id: uuid.UUID, body: bytes) -> str:
    """Bind a key to the tenant, operation and exact payload."""
    canonical = b"\x00".join(
        (method.upper().encode(), path.encode(), str(tenant_id).encode(), body)
    )
    return hashlib.sha256(canonical).hexdigest()


@dataclass(frozen=True, slots=True)
class IdempotencyRecord:
    """Immutable replay metadata; response bodies remain outside the ledger."""

    fingerprint: str
    status_code: int
    resource_id: str
    expires_at: int


class IdempotencyLedger:
    """Bounded process-local replay detector for single-instance/API tests."""

    def __init__(self, *, ttl_seconds: int = 86_400, max_records: int = 10_000) -> None:
        if not 1 <= ttl_seconds <= 604_800 or not 1 <= max_records <= 100_000:
            raise ValueError("idempotency ledger bounds are invalid")
        self._ttl_seconds = ttl_seconds
        self._max_records = max_records
        self._records: dict[tuple[uuid.UUID, str], IdempotencyRecord] = {}
        self._lock = threading.RLock()

    def resolve(
        self,
        *,
        tenant_id: uuid.UUID,
        key: str,
        fingerprint: str,
        now: int | None = None,
    ) -> IdempotencyRecord | None:
        """Return a safe replay, reject payload reuse, or reserve a new key."""
        validate_idempotency_key(key)
        if not _HEX_DIGEST.fullmatch(fingerprint):
            raise ValueError("fingerprint must be a lowercase SHA-256 digest")
        current_time = int(time.time()) if now is None else now
        identity = (tenant_id, key)
        with self._lock:
            record = self._records.get(identity)
            if record is None or record.expires_at <= current_time:
                self._records.pop(identity, None)
                return None
            if not hmac.compare_digest(record.fingerprint, fingerprint):
                raise APIContractError(
                    status=409,
                    code="IDEMPOTENCY_CONFLICT",
                    title="Idempotency key conflict",
                    detail="Idempotency key was already used for a different request",
                )
            return record

    def commit(
        self,
        *,
        tenant_id: uuid.UUID,
        key: str,
        fingerprint: str,
        status_code: int,
        resource_id: str,
        now: int | None = None,
    ) -> IdempotencyRecord:
        """Commit bounded replay metadata after a successful mutation."""
        current_time = int(time.time()) if now is None else now
        with self._lock:
            existing = self.resolve(
                tenant_id=tenant_id,
                key=key,
                fingerprint=fingerprint,
                now=current_time,
            )
            if existing is not None:
                return existing
            active = {
                identity: record
                for identity, record in self._records.items()
                if record.expires_at > current_time
            }
            if len(active) >= self._max_records:
                raise APIContractError(
                    status=503,
                    code="IDEMPOTENCY_CAPACITY_EXHAUSTED",
                    title="Idempotency capacity exhausted",
                    detail="Idempotency ledger cannot safely accept another key",
                )
            record = IdempotencyRecord(
                fingerprint=fingerprint,
                status_code=status_code,
                resource_id=resource_id,
                expires_at=current_time + self._ttl_seconds,
            )
            active[(tenant_id, key)] = record
            self._records = active
            return record


def strong_etag(*, resource_version: int, representation_digest: str) -> str:
    """Build a strong validator from an immutable version and representation digest."""
    if resource_version < 1 or not _HEX_DIGEST.fullmatch(representation_digest):
        raise ValueError("ETag inputs are invalid")
    token = hashlib.sha256(f"{resource_version}:{representation_digest}".encode()).hexdigest()
    return f'"{token}"'


def require_if_match(value: str | None, *, current_etag: str) -> None:
    """Require exact optimistic-concurrency fencing for state-changing operations."""
    if value is None:
        raise APIContractError(
            status=428,
            code="IF_MATCH_REQUIRED",
            title="Precondition required",
            detail=f"{IF_MATCH_HEADER} is required for this operation",
        )
    candidates = {candidate.strip() for candidate in value.split(",")}
    if "*" in candidates or current_etag not in candidates:
        raise APIContractError(
            status=412,
            code="ETAG_MISMATCH",
            title="Precondition failed",
            detail="Resource representation changed before this operation",
        )


class CursorCodec:
    """Encode tamper-evident, tenant/query-bound pagination cursors."""

    def __init__(self, signing_key: bytes, *, ttl_seconds: int = 900) -> None:
        if len(signing_key) < 32 or not 1 <= ttl_seconds <= 86_400:
            raise ValueError("cursor signing key or lifetime is invalid")
        self._signing_key = signing_key
        self._ttl_seconds = ttl_seconds

    @staticmethod
    def _b64encode(value: bytes) -> str:
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode()

    @staticmethod
    def _b64decode(value: str) -> bytes:
        padding = "=" * (-len(value) % 4)
        return base64.b64decode(value + padding, altchars=b"-_", validate=True)

    def encode(
        self,
        *,
        tenant_id: uuid.UUID,
        query_digest: str,
        after: str,
        now: int | None = None,
    ) -> str:
        """Create an opaque cursor with a bounded lifetime."""
        if not _HEX_DIGEST.fullmatch(query_digest) or not 1 <= len(after) <= 256:
            raise ValueError("cursor claims are invalid")
        current_time = int(time.time()) if now is None else now
        payload = json.dumps(
            {
                "after": after,
                "exp": current_time + self._ttl_seconds,
                "query": query_digest,
                "tenant": str(tenant_id),
                "v": 1,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
        signature = hmac.digest(self._signing_key, payload, "sha256")
        return f"{self._b64encode(payload)}.{self._b64encode(signature)}"

    def decode(
        self,
        cursor: str,
        *,
        tenant_id: uuid.UUID,
        query_digest: str,
        now: int | None = None,
    ) -> str:
        """Verify integrity, expiry, tenant and query binding before returning position."""
        try:
            encoded_payload, encoded_signature = cursor.split(".", 1)
            payload = self._b64decode(encoded_payload)
            signature = self._b64decode(encoded_signature)
            claims = json.loads(payload)
        except (ValueError, TypeError, json.JSONDecodeError):
            self._invalid_cursor()
        expected = hmac.digest(self._signing_key, payload, "sha256")
        if not hmac.compare_digest(signature, expected):
            self._invalid_cursor()
        current_time = int(time.time()) if now is None else now
        after = claims.get("after") if isinstance(claims, dict) else None
        if (
            not isinstance(claims, dict)
            or claims.get("v") != 1
            or claims.get("tenant") != str(tenant_id)
            or claims.get("query") != query_digest
            or not isinstance(claims.get("exp"), int)
            or claims["exp"] <= current_time
            or not isinstance(after, str)
        ):
            self._invalid_cursor()
        return after

    @staticmethod
    def _invalid_cursor() -> NoReturn:
        raise APIContractError(
            status=400,
            code="INVALID_CURSOR",
            title="Invalid pagination cursor",
            detail="Cursor is malformed, expired, tampered with, or outside request scope",
        )


def bounded_page_size(value: int | None, *, budget: RequestBudget) -> int:
    """Apply the server default and reject client requests above the declared ceiling."""
    page_size = min(50, budget.max_page_size) if value is None else value
    if not 1 <= page_size <= budget.max_page_size:
        raise APIContractError(
            status=400,
            code="INVALID_PAGE_SIZE",
            title="Invalid page size",
            detail=f"Page size must be between 1 and {budget.max_page_size}",
        )
    return page_size


def query_fingerprint(parameters: Mapping[str, str]) -> str:
    """Bind cursors to a deterministic set of normalized filter parameters."""
    encoded = json.dumps(dict(sorted(parameters.items())), separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
