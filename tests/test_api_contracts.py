"""Enterprise API error, correlation, replay, concurrency and pagination contracts."""

import asyncio
import hashlib
import uuid

import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel

from ailora.api.contracts import (
    CORRELATION_HEADER,
    PROBLEM_MEDIA_TYPE,
    APIContractError,
    APIContractMiddleware,
    CursorCodec,
    IdempotencyLedger,
    RequestBudget,
    api_contract_error_handler,
    bounded_page_size,
    http_exception_handler,
    idempotency_fingerprint,
    query_fingerprint,
    require_if_match,
    strong_etag,
    validate_idempotency_key,
    validation_error_handler,
)
from ailora.config import Settings

TENANT_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")
OTHER_TENANT_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")
CORRELATION_ID = uuid.UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
SIGNING_KEY = b"0123456789abcdef0123456789abcdef"
BUDGET = RequestBudget(max_body_bytes=64, timeout_seconds=0.05, max_page_size=100)


class Input(BaseModel):
    name: str


def _app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(APIContractMiddleware, budget=BUDGET)
    app.add_exception_handler(APIContractError, api_contract_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

    @app.get("/ok")
    async def ok(request: Request) -> dict[str, str]:
        return {"correlation_id": str(request.state.correlation_id)}

    @app.get("/rejected")
    async def rejected() -> None:
        raise HTTPException(status_code=403, detail="access denied")

    @app.post("/validated")
    async def validated(value: Input) -> Input:
        return value

    @app.get("/slow")
    async def slow() -> None:
        await asyncio.sleep(0.2)

    return app


def test_correlation_id_is_generated_and_echoed() -> None:
    response = TestClient(_app()).get("/ok")
    correlation_id = uuid.UUID(response.headers[CORRELATION_HEADER])
    assert response.json() == {"correlation_id": str(correlation_id)}
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_valid_correlation_id_is_preserved() -> None:
    response = TestClient(_app()).get("/ok", headers={CORRELATION_HEADER: str(CORRELATION_ID)})
    assert response.headers[CORRELATION_HEADER] == str(CORRELATION_ID)


def test_invalid_correlation_id_returns_problem_details() -> None:
    response = TestClient(_app()).get("/ok", headers={CORRELATION_HEADER: "unsafe value"})
    body = response.json()
    assert response.status_code == 400
    assert response.headers["content-type"].startswith(PROBLEM_MEDIA_TYPE)
    assert body["code"] == "INVALID_CORRELATION_ID"
    assert body["status"] == 400
    assert body["instance"] == "/ok"
    assert body["correlation_id"] == response.headers[CORRELATION_HEADER]


def test_http_exception_is_normalized_without_losing_correlation() -> None:
    response = TestClient(_app()).get(
        "/rejected", headers={CORRELATION_HEADER: str(CORRELATION_ID)}
    )
    assert response.status_code == 403
    assert response.json()["code"] == "HTTP_403"
    assert response.json()["detail"] == "access denied"
    assert response.headers[CORRELATION_HEADER] == str(CORRELATION_ID)


def test_validation_error_does_not_reflect_raw_input() -> None:
    response = TestClient(_app()).post("/validated", json={"name": 123})
    assert response.status_code == 422
    assert response.json()["code"] == "REQUEST_VALIDATION_FAILED"
    assert "123" not in response.text


def test_declared_body_over_budget_is_rejected_before_routing() -> None:
    response = TestClient(_app()).post("/validated", content=b"x" * 65)
    assert response.status_code == 413
    assert response.json()["code"] == "REQUEST_BODY_TOO_LARGE"


def test_processing_timeout_is_bounded_problem() -> None:
    response = TestClient(_app(), raise_server_exceptions=False).get("/slow")
    assert response.status_code == 504
    assert response.json()["code"] == "REQUEST_BUDGET_EXHAUSTED"


@pytest.mark.parametrize("value", [None, "short", "has spaces and unsafe!", "x" * 129])
def test_idempotency_key_validation_is_fail_closed(value: str | None) -> None:
    with pytest.raises(APIContractError) as error:
        validate_idempotency_key(value)
    assert error.value.status == 400


def test_idempotency_fingerprint_binds_tenant_operation_and_body() -> None:
    first = idempotency_fingerprint(
        method="post", path="/v1/resources", tenant_id=TENANT_ID, body=b'{"x":1}'
    )
    assert len(first) == 64
    assert first != idempotency_fingerprint(
        method="post", path="/v1/resources", tenant_id=OTHER_TENANT_ID, body=b'{"x":1}'
    )
    assert first != idempotency_fingerprint(
        method="post", path="/v1/resources", tenant_id=TENANT_ID, body=b'{"x":2}'
    )


def test_idempotency_ledger_replays_same_request() -> None:
    ledger = IdempotencyLedger(ttl_seconds=60, max_records=2)
    fingerprint = hashlib.sha256(b"request").hexdigest()
    record = ledger.commit(
        tenant_id=TENANT_ID,
        key="stable-request-0001",
        fingerprint=fingerprint,
        status_code=201,
        resource_id="resource-1",
        now=100,
    )
    assert (
        ledger.resolve(
            tenant_id=TENANT_ID,
            key="stable-request-0001",
            fingerprint=fingerprint,
            now=101,
        )
        == record
    )


def test_idempotency_ledger_rejects_key_reuse_with_different_payload() -> None:
    ledger = IdempotencyLedger(ttl_seconds=60)
    ledger.commit(
        tenant_id=TENANT_ID,
        key="stable-request-0001",
        fingerprint=hashlib.sha256(b"first").hexdigest(),
        status_code=201,
        resource_id="resource-1",
        now=100,
    )
    with pytest.raises(APIContractError) as error:
        ledger.resolve(
            tenant_id=TENANT_ID,
            key="stable-request-0001",
            fingerprint=hashlib.sha256(b"second").hexdigest(),
            now=101,
        )
    assert error.value.status == 409


def test_expired_idempotency_record_can_be_replaced() -> None:
    ledger = IdempotencyLedger(ttl_seconds=2)
    first = hashlib.sha256(b"first").hexdigest()
    second = hashlib.sha256(b"second").hexdigest()
    ledger.commit(
        tenant_id=TENANT_ID,
        key="stable-request-0001",
        fingerprint=first,
        status_code=201,
        resource_id="resource-1",
        now=100,
    )
    assert (
        ledger.resolve(
            tenant_id=TENANT_ID,
            key="stable-request-0001",
            fingerprint=second,
            now=102,
        )
        is None
    )


def test_idempotency_capacity_fails_closed() -> None:
    ledger = IdempotencyLedger(ttl_seconds=60, max_records=1)
    ledger.commit(
        tenant_id=TENANT_ID,
        key="stable-request-0001",
        fingerprint=hashlib.sha256(b"first").hexdigest(),
        status_code=201,
        resource_id="resource-1",
        now=100,
    )
    with pytest.raises(APIContractError) as error:
        ledger.commit(
            tenant_id=TENANT_ID,
            key="stable-request-0002",
            fingerprint=hashlib.sha256(b"second").hexdigest(),
            status_code=201,
            resource_id="resource-2",
            now=101,
        )
    assert error.value.status == 503


def test_etag_is_strong_and_deterministic() -> None:
    digest = hashlib.sha256(b"representation").hexdigest()
    first = strong_etag(resource_version=3, representation_digest=digest)
    assert first.startswith('"') and first.endswith('"')
    assert first == strong_etag(resource_version=3, representation_digest=digest)
    assert first != strong_etag(resource_version=4, representation_digest=digest)


def test_if_match_is_required() -> None:
    with pytest.raises(APIContractError) as error:
        require_if_match(None, current_etag='"current"')
    assert error.value.status == 428


@pytest.mark.parametrize("value", ['"stale"', "*", 'W/"current"'])
def test_if_match_rejects_stale_wildcard_and_weak_validators(value: str) -> None:
    with pytest.raises(APIContractError) as error:
        require_if_match(value, current_etag='"current"')
    assert error.value.status == 412


def test_if_match_accepts_exact_validator_from_list() -> None:
    require_if_match('"old", "current"', current_etag='"current"')


def test_cursor_round_trip_is_tenant_and_query_bound() -> None:
    codec = CursorCodec(SIGNING_KEY, ttl_seconds=60)
    query = query_fingerprint({"sort": "created_at", "state": "open"})
    cursor = codec.encode(tenant_id=TENANT_ID, query_digest=query, after="resource-9", now=100)
    assert codec.decode(cursor, tenant_id=TENANT_ID, query_digest=query, now=101) == "resource-9"


def test_cursor_tampering_is_rejected() -> None:
    codec = CursorCodec(SIGNING_KEY, ttl_seconds=60)
    query = query_fingerprint({"sort": "created_at"})
    cursor = codec.encode(tenant_id=TENANT_ID, query_digest=query, after="resource-9", now=100)
    with pytest.raises(APIContractError) as error:
        codec.decode(f"x{cursor}", tenant_id=TENANT_ID, query_digest=query, now=101)
    assert error.value.code == "INVALID_CURSOR"


def test_cursor_cross_tenant_replay_is_rejected() -> None:
    codec = CursorCodec(SIGNING_KEY, ttl_seconds=60)
    query = query_fingerprint({"sort": "created_at"})
    cursor = codec.encode(tenant_id=TENANT_ID, query_digest=query, after="resource-9", now=100)
    with pytest.raises(APIContractError):
        codec.decode(cursor, tenant_id=OTHER_TENANT_ID, query_digest=query, now=101)


def test_expired_cursor_is_rejected() -> None:
    codec = CursorCodec(SIGNING_KEY, ttl_seconds=2)
    query = query_fingerprint({"sort": "created_at"})
    cursor = codec.encode(tenant_id=TENANT_ID, query_digest=query, after="resource-9", now=100)
    with pytest.raises(APIContractError):
        codec.decode(cursor, tenant_id=TENANT_ID, query_digest=query, now=102)


@pytest.mark.parametrize("value, expected", [(None, 50), (1, 1), (100, 100)])
def test_page_size_accepts_bounded_values(value: int | None, expected: int) -> None:
    assert bounded_page_size(value, budget=BUDGET) == expected


@pytest.mark.parametrize("value", [0, 101, -1])
def test_page_size_rejects_out_of_budget_values(value: int) -> None:
    with pytest.raises(APIContractError):
        bounded_page_size(value, budget=BUDGET)


def test_runtime_settings_publish_bounded_api_defaults() -> None:
    settings = Settings(_env_file=None)
    assert settings.api_max_body_bytes == 1_048_576
    assert settings.api_request_timeout_seconds == 15.0
    assert settings.api_max_page_size == 100
