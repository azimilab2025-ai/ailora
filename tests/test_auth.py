"""
AILORA P2-02: JWT Authentication Middleware Contract Tests.

Validates:
- hash_password / verify_password contract (bcrypt, no plaintext stored)
- create_access_token produces a valid signed JWT
- decode_access_token validates and rejects invalid/expired tokens
- require_authenticated_user dependency returns 401 on missing/bad token
- No secret leaks in error messages
- TokenError is raised appropriately
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from ailora.security.auth import (
    TokenError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from ailora.security.dependencies import require_authenticated_user

# ─── Password hashing ─────────────────────────────────────────────────────────


def test_hash_password_returns_hash() -> None:
    h = hash_password("secret123")
    assert h.startswith("$2b$") or h.startswith("$2a$")


def test_hash_password_not_plaintext() -> None:
    h = hash_password("mysecret")
    assert "mysecret" not in h


def test_verify_password_correct() -> None:
    h = hash_password("mypassword")
    assert verify_password("mypassword", h) is True


def test_verify_password_wrong() -> None:
    h = hash_password("mypassword")
    assert verify_password("wrongpw", h) is False


def test_hash_is_non_deterministic() -> None:
    """Each call to hash_password should produce a different salt."""
    h1 = hash_password("samepass")
    h2 = hash_password("samepass")
    assert h1 != h2


# ─── Token creation ───────────────────────────────────────────────────────────


def test_create_access_token_returns_string() -> None:
    token = create_access_token("user-uuid-123")
    assert isinstance(token, str)
    assert len(token) > 20


def test_create_access_token_with_extra_claims() -> None:
    token = create_access_token("user-uuid-123", extra_claims={"tenant_id": "t1"})
    payload = decode_access_token(token)
    assert payload["tenant_id"] == "t1"


def test_create_access_token_has_sub_claim() -> None:
    token = create_access_token("user-uuid-abc")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-uuid-abc"


def test_create_access_token_has_exp_claim() -> None:
    token = create_access_token("user-uuid-abc")
    payload = decode_access_token(token)
    assert "exp" in payload
    exp_dt = datetime.fromtimestamp(payload["exp"], tz=UTC)
    assert exp_dt > datetime.now(tz=UTC)


# ─── Token decoding and validation ────────────────────────────────────────────


def test_decode_valid_token() -> None:
    token = create_access_token("user-id-1")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-id-1"


def test_decode_invalid_token_raises_token_error() -> None:
    with pytest.raises(TokenError):
        decode_access_token("not.a.valid.jwt")


def test_decode_tampered_token_raises_token_error() -> None:
    token = create_access_token("user-id-1")
    tampered = token[:-5] + "XXXXX"
    with pytest.raises(TokenError):
        decode_access_token(tampered)


def test_decode_expired_token_raises_token_error() -> None:
    from jose import jwt as jose_jwt

    from ailora.config import settings

    payload = {
        "sub": "user-id-exp",
        "exp": datetime.now(tz=UTC) - timedelta(seconds=1),
    }
    expired_token = jose_jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    with pytest.raises(TokenError):
        decode_access_token(expired_token)


def test_token_error_message_does_not_expose_secret() -> None:
    """TokenError messages must not contain the secret key."""
    from ailora.config import settings

    try:
        decode_access_token("invalid.token")
    except TokenError as e:
        assert settings.secret_key not in str(e)


# ─── FastAPI dependency integration ──────────────────────────────────────────


def _make_protected_app() -> FastAPI:
    """Create a minimal FastAPI app with a protected route for testing."""
    from typing import Any

    from fastapi import Depends

    app = FastAPI()

    @app.get("/protected")
    async def protected(
        token_data: dict[str, Any] = Depends(require_authenticated_user),  # noqa: B008
    ) -> dict[str, Any]:
        return {"sub": token_data["sub"]}

    return app


@pytest.mark.asyncio
async def test_protected_route_with_valid_token() -> None:
    app = _make_protected_app()
    token = create_access_token("user-xyz")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["sub"] == "user-xyz"


@pytest.mark.asyncio
async def test_protected_route_no_token_returns_401() -> None:
    app = _make_protected_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_invalid_token_returns_401() -> None:
    app = _make_protected_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected", headers={"Authorization": "Bearer invalid.token"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_error_body_no_secret() -> None:
    """401 response body must not contain the secret key."""
    from ailora.config import settings

    app = _make_protected_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected", headers={"Authorization": "Bearer bad.token.here"})
    assert settings.secret_key not in resp.text


@pytest.mark.asyncio
async def test_protected_route_wrong_scheme_returns_401() -> None:
    """Basic auth scheme must be rejected (not Bearer)."""
    app = _make_protected_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected", headers={"Authorization": "Basic dXNlcjpwYXNz"})
    assert resp.status_code == 401


# ─── Sync client test for simple cases ───────────────────────────────────────


def test_protected_route_sync_no_token() -> None:
    app = _make_protected_app()
    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/protected")
    assert resp.status_code == 401
