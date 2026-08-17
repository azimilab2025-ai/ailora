"""Asymmetric JWT, JWKS, and bounded key-rotation contracts."""

from __future__ import annotations

import base64
import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ailora.security.asymmetric_tokens import (
    AsymmetricTokenError,
    AsymmetricTokenProfile,
    JwtSigningKey,
    RotatingJwtKeyRing,
    decode_access_token,
    issue_access_token,
)


def _signing_key(kid: str, *, bits: int = 2048) -> JwtSigningKey:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    return JwtSigningKey.from_private_pem(kid=kid, private_key_pem=private_pem)


@pytest.fixture(scope="module")
def key_one() -> JwtSigningKey:
    return _signing_key("key-2026-01")


@pytest.fixture(scope="module")
def key_two() -> JwtSigningKey:
    return _signing_key("key-2026-02")


@pytest.fixture
def profile() -> AsymmetricTokenProfile:
    return AsymmetricTokenProfile(
        issuer="https://identity.ailora.example/",
        audience="ailora-api",
    )


def _ring(key: JwtSigningKey) -> RotatingJwtKeyRing:
    return RotatingJwtKeyRing(keys=[key], active_kid=key.kid)


def _replace_header(token: str, **changes: str) -> str:
    encoded_header, payload, signature = token.split(".")
    padding = "=" * (-len(encoded_header) % 4)
    header = json.loads(base64.urlsafe_b64decode(encoded_header + padding))
    header.update(changes)
    replacement = base64.urlsafe_b64encode(
        json.dumps(header, separators=(",", ":")).encode()
    ).rstrip(b"=")
    return b".".join((replacement, payload.encode(), signature.encode())).decode()


def test_round_trip_requires_issuer_audience_jti_and_kid(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token_id = uuid4()
    ring = _ring(key_one)
    token = issue_access_token(
        subject="user-123",
        key_ring=ring,
        profile=profile,
        extra_claims={"tenant_id": "tenant-1"},
        now=now,
        jti=token_id,
    )
    payload = decode_access_token(token, key_ring=ring, profile=profile)

    assert payload["iss"] == "https://identity.ailora.example"
    assert payload["aud"] == "ailora-api"
    assert payload["jti"] == str(token_id)
    assert payload["tenant_id"] == "tenant-1"
    assert jwt.get_unverified_header(token) == {
        "alg": "RS256",
        "kid": "key-2026-01",
        "typ": "JWT",
    }


def test_wrong_issuer_or_audience_fails_closed(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    ring = _ring(key_one)
    token = issue_access_token(subject="user-1", key_ring=ring, profile=profile)

    for wrong_profile in (
        AsymmetricTokenProfile(issuer="https://wrong.example", audience=profile.audience),
        AsymmetricTokenProfile(issuer=profile.issuer, audience="wrong-api"),
    ):
        with pytest.raises(AsymmetricTokenError, match="token validation failed"):
            decode_access_token(token, key_ring=ring, profile=wrong_profile)


def test_algorithm_confusion_and_unknown_kid_fail_before_key_use(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    ring = _ring(key_one)
    token = issue_access_token(subject="user-1", key_ring=ring, profile=profile)

    with pytest.raises(AsymmetricTokenError, match="token validation failed"):
        decode_access_token(_replace_header(token, alg="HS256"), key_ring=ring, profile=profile)
    with pytest.raises(AsymmetricTokenError, match="token validation failed"):
        decode_access_token(_replace_header(token, kid="unknown"), key_ring=ring, profile=profile)


def test_rotation_preserves_old_verification_but_removes_old_signing_material(
    key_one: JwtSigningKey,
    key_two: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    first_ring = _ring(key_one)
    old_token = issue_access_token(subject="old", key_ring=first_ring, profile=profile)
    rotated = first_ring.rotate(key_two)
    new_token = issue_access_token(subject="new", key_ring=rotated, profile=profile)

    assert decode_access_token(old_token, key_ring=rotated, profile=profile)["sub"] == "old"
    assert decode_access_token(new_token, key_ring=rotated, profile=profile)["sub"] == "new"
    assert rotated.active_signing_key.kid == key_two.kid
    assert rotated.resolve_verification_key(key_one.kid).private_key_pem is None
    with pytest.raises(AsymmetricTokenError):
        decode_access_token(new_token, key_ring=first_ring, profile=profile)


def test_jwks_is_deterministic_public_only(
    key_one: JwtSigningKey,
    key_two: JwtSigningKey,
) -> None:
    jwks = _ring(key_one).rotate(key_two).public_jwks()

    assert [record["kid"] for record in jwks["keys"]] == [key_one.kid, key_two.kid]
    assert all(record["alg"] == "RS256" and record["use"] == "sig" for record in jwks["keys"])
    assert all(record["kty"] == "RSA" for record in jwks["keys"])
    assert all(
        not {"d", "p", "q", "dp", "dq", "qi"}.intersection(record) for record in jwks["keys"]
    )


def test_expired_token_and_malformed_jti_are_rejected(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    ring = _ring(key_one)
    expired = issue_access_token(
        subject="expired",
        key_ring=ring,
        profile=profile,
        now=datetime.now(UTC) - timedelta(hours=1),
    )
    malformed_jti = issue_access_token(
        subject="bad-jti",
        key_ring=ring,
        profile=profile,
        jti=uuid4(),
    )
    parts = malformed_jti.split(".")
    unverified = jwt.decode(malformed_jti, options={"verify_signature": False})
    unverified["jti"] = "not-a-uuid"
    assert len(parts) == 3
    malformed_jti = jwt.encode(
        unverified,
        key_one.private_key_pem,
        algorithm="RS256",
        headers={"kid": key_one.kid, "typ": "JWT"},
    )

    with pytest.raises(AsymmetricTokenError):
        decode_access_token(expired, key_ring=ring, profile=profile)
    with pytest.raises(AsymmetricTokenError):
        decode_access_token(malformed_jti, key_ring=ring, profile=profile)


def test_reserved_claims_subject_and_naive_time_are_rejected(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    ring = _ring(key_one)
    with pytest.raises(ValueError, match="reserved claims"):
        issue_access_token(
            subject="user",
            key_ring=ring,
            profile=profile,
            extra_claims={"iss": "https://attacker.example"},
        )
    with pytest.raises(ValueError, match="subject"):
        issue_access_token(subject=" ", key_ring=ring, profile=profile)
    with pytest.raises(ValueError, match="timezone-aware"):
        issue_access_token(
            subject="user",
            key_ring=ring,
            profile=profile,
            now=datetime(2026, 1, 1),
        )


def test_profile_and_leeway_are_bounded(
    key_one: JwtSigningKey,
    profile: AsymmetricTokenProfile,
) -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        AsymmetricTokenProfile(issuer="http://identity.example", audience="api")
    with pytest.raises(ValueError, match="audience"):
        AsymmetricTokenProfile(issuer="https://identity.example", audience=" ")
    with pytest.raises(ValueError, match="lifetime"):
        AsymmetricTokenProfile(
            issuer="https://identity.example",
            audience="api",
            access_token_ttl=timedelta(hours=2),
        )
    token = issue_access_token(subject="user", key_ring=_ring(key_one), profile=profile)
    with pytest.raises(ValueError, match="leeway"):
        decode_access_token(token, key_ring=_ring(key_one), profile=profile, leeway_seconds=31)


def test_key_ring_rejects_duplicates_missing_signer_and_unsafe_identifiers(
    key_one: JwtSigningKey,
) -> None:
    with pytest.raises(ValueError, match="unique"):
        RotatingJwtKeyRing(keys=[key_one, key_one], active_kid=key_one.kid)
    with pytest.raises(ValueError, match="active key"):
        RotatingJwtKeyRing(keys=[key_one.verification_only()], active_kid=key_one.kid)
    with pytest.raises(ValueError, match="identifier"):
        JwtSigningKey.from_private_pem(
            kid="unsafe key!",
            private_key_pem=key_one.private_key_pem or "",
        )


def test_key_ring_rejects_weak_rsa_and_duplicate_rotation(
    key_one: JwtSigningKey,
) -> None:
    with pytest.raises(ValueError, match="2048"):
        _signing_key("weak-key", bits=1024)
    with pytest.raises(ValueError, match="new key identifier"):
        _ring(key_one).rotate(key_one)
