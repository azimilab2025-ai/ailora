"""Provider-neutral OIDC, MFA, and hardened session lifecycle contracts."""

from __future__ import annotations

import base64
import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ailora.security.asymmetric_tokens import JwtSigningKey, RotatingJwtKeyRing
from ailora.security.oidc_sessions import (
    HardenedSessionPolicy,
    OidcIdTokenVerifier,
    OidcProviderProfile,
    OidcValidationError,
)

NONCE = "nonce-with-at-least-sixteen-characters"


@pytest.fixture(scope="module")
def signing_key() -> JwtSigningKey:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    return JwtSigningKey.from_private_pem(kid="idp-key-01", private_key_pem=private_pem)


@pytest.fixture
def profile() -> OidcProviderProfile:
    return OidcProviderProfile(
        issuer="https://idp.ailora.example/",
        client_id="ailora-web",
        mfa_acr_values=frozenset({"urn:ailora:acr:mfa"}),
    )


def _jwks(signing_key: JwtSigningKey) -> dict[str, list[dict[str, object]]]:
    return RotatingJwtKeyRing(keys=[signing_key], active_kid=signing_key.kid).public_jwks()


def _token(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
    *,
    now: datetime | None = None,
    claims: dict[str, object] | None = None,
    headers: dict[str, object] | None = None,
) -> str:
    issued_at = now or datetime.now(UTC)
    payload: dict[str, object] = {
        "iss": profile.issuer,
        "sub": "provider-user-123",
        "aud": profile.client_id,
        "exp": issued_at + timedelta(minutes=10),
        "iat": issued_at,
        "auth_time": issued_at,
        "nonce": NONCE,
        "sid": "provider-session-123",
        "acr": "urn:ailora:acr:mfa",
        "amr": ["pwd", "otp"],
        "email": "Operator@Example.Test",
        "email_verified": True,
        **(claims or {}),
    }
    for numeric_date_claim in ("exp", "iat", "auth_time"):
        value = payload[numeric_date_claim]
        if isinstance(value, datetime):
            payload[numeric_date_claim] = int(value.timestamp())
    return jwt.encode(
        payload,
        signing_key.private_key_pem,
        algorithm="RS256",
        headers={"kid": signing_key.kid, "typ": "JWT", **(headers or {})},
    )


def _verifier(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> OidcIdTokenVerifier:
    return OidcIdTokenVerifier(profile=profile, jwks=_jwks(signing_key))


def _replace_header(token: str, **changes: str) -> str:
    encoded_header, payload, signature = token.split(".")
    padding = "=" * (-len(encoded_header) % 4)
    header = json.loads(base64.urlsafe_b64decode(encoded_header + padding))
    header.update(changes)
    replacement = base64.urlsafe_b64encode(
        json.dumps(header, separators=(",", ":")).encode()
    ).rstrip(b"=")
    return b".".join((replacement, payload.encode(), signature.encode())).decode()


def test_verified_oidc_principal_preserves_mfa_and_verified_email(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    principal = _verifier(signing_key, profile).verify(
        _token(signing_key, profile),
        expected_nonce=NONCE,
    )

    assert principal.issuer == "https://idp.ailora.example"
    assert principal.subject == "provider-user-123"
    assert principal.provider_session_id == "provider-session-123"
    assert principal.mfa_authenticated is True
    assert principal.amr == ("otp", "pwd")
    assert principal.verified_email == "operator@example.test"


def test_wrong_nonce_issuer_and_audience_fail_closed(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    verifier = _verifier(signing_key, profile)
    cases = (
        (_token(signing_key, profile), "different-nonce-at-least-sixteen"),
        (_token(signing_key, profile, claims={"iss": "https://wrong.example"}), NONCE),
        (_token(signing_key, profile, claims={"aud": "wrong-client"}), NONCE),
    )
    for token, nonce in cases:
        with pytest.raises(OidcValidationError, match="OIDC validation failed"):
            verifier.verify(token, expected_nonce=nonce)


def test_unknown_kid_algorithm_confusion_and_remote_key_headers_are_rejected(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    verifier = _verifier(signing_key, profile)
    valid = _token(signing_key, profile)
    tokens = (
        _replace_header(valid, kid="unknown"),
        _replace_header(valid, alg="HS256"),
        _token(signing_key, profile, headers={"jku": "https://attacker.example/jwks"}),
        _token(signing_key, profile, headers={"x5u": "https://attacker.example/cert"}),
    )
    for token in tokens:
        with pytest.raises(OidcValidationError, match="OIDC validation failed"):
            verifier.verify(token, expected_nonce=NONCE)


def test_jwks_rejects_private_material_duplicate_and_wrong_use(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    public_record = _jwks(signing_key)["keys"][0]
    private_record = {**public_record, "d": "private"}
    with pytest.raises(ValueError, match="private key material"):
        OidcIdTokenVerifier(profile=profile, jwks={"keys": [private_record]})
    with pytest.raises(ValueError, match="unique"):
        OidcIdTokenVerifier(profile=profile, jwks={"keys": [public_record, public_record]})
    with pytest.raises(ValueError, match="RS256"):
        OidcIdTokenVerifier(
            profile=profile,
            jwks={"keys": [{**public_record, "use": "enc"}]},
        )


def test_multiple_audiences_require_exact_authorized_party(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    verifier = _verifier(signing_key, profile)
    accepted = _token(
        signing_key,
        profile,
        claims={"aud": [profile.client_id, "another-client"], "azp": profile.client_id},
    )
    rejected = _token(
        signing_key,
        profile,
        claims={"aud": [profile.client_id, "another-client"], "azp": "another-client"},
    )

    assert verifier.verify(accepted, expected_nonce=NONCE).subject == "provider-user-123"
    with pytest.raises(OidcValidationError):
        verifier.verify(rejected, expected_nonce=NONCE)


def test_mfa_needs_both_allowed_acr_and_mfa_method_and_email_verification(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    verifier = _verifier(signing_key, profile)
    no_acr = verifier.verify(
        _token(signing_key, profile, claims={"acr": "urn:weak", "amr": ["otp"]}),
        expected_nonce=NONCE,
    )
    no_method = verifier.verify(
        _token(signing_key, profile, claims={"amr": ["pwd"]}),
        expected_nonce=NONCE,
    )
    unverified_email = verifier.verify(
        _token(signing_key, profile, claims={"email_verified": False}),
        expected_nonce=NONCE,
    )

    assert no_acr.mfa_authenticated is False
    assert no_method.mfa_authenticated is False
    assert unverified_email.verified_email is None


def test_stale_id_token_and_future_authentication_time_are_rejected(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    verifier = _verifier(signing_key, profile)
    stale = _token(
        signing_key,
        profile,
        now=now - timedelta(minutes=6),
        claims={"exp": now + timedelta(minutes=5)},
    )
    future_auth = _token(
        signing_key,
        profile,
        now=now,
        claims={"auth_time": now + timedelta(minutes=2)},
    )

    with pytest.raises(OidcValidationError):
        verifier.verify(stale, expected_nonce=NONCE, now=now)
    with pytest.raises(OidcValidationError):
        verifier.verify(future_auth, expected_nonce=NONCE, now=now)


def test_refresh_rotation_is_single_use_and_family_bound(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, profile).verify(
        _token(signing_key, profile, now=now),
        expected_nonce=NONCE,
        now=now,
    )
    policy = HardenedSessionPolicy()
    state = policy.start(principal, now=now)
    rotated = policy.rotate(
        state,
        presented_family_id=state.refresh_family_id,
        presented_rotation_counter=0,
        now=now + timedelta(minutes=1),
    )

    assert rotated.rotation_counter == 1
    with pytest.raises(OidcValidationError, match="session validation failed"):
        policy.rotate(
            rotated,
            presented_family_id=rotated.refresh_family_id,
            presented_rotation_counter=0,
            now=now + timedelta(minutes=2),
        )
    with pytest.raises(OidcValidationError):
        policy.rotate(
            rotated,
            presented_family_id=uuid4(),
            presented_rotation_counter=1,
            now=now + timedelta(minutes=2),
        )


def test_idle_absolute_expiry_and_logout_block_rotation(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, profile).verify(
        _token(signing_key, profile, now=now),
        expected_nonce=NONCE,
        now=now,
    )
    policy = HardenedSessionPolicy(
        absolute_lifetime=timedelta(minutes=10),
        idle_timeout=timedelta(minutes=2),
    )
    state = policy.start(principal, now=now)
    for blocked_state, checked_at in (
        (state, now + timedelta(minutes=3)),
        (state, now + timedelta(minutes=10)),
        (policy.logout(state, now=now + timedelta(minutes=1)), now + timedelta(minutes=1)),
    ):
        with pytest.raises(OidcValidationError):
            policy.rotate(
                blocked_state,
                presented_family_id=blocked_state.refresh_family_id,
                presented_rotation_counter=blocked_state.rotation_counter,
                now=checked_at,
            )


def test_privileged_effect_requires_recent_verified_mfa(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    verifier = _verifier(signing_key, profile)
    policy = HardenedSessionPolicy(privileged_mfa_max_age=timedelta(minutes=5))
    mfa_state = policy.start(
        verifier.verify(
            _token(signing_key, profile, now=now),
            expected_nonce=NONCE,
            now=now,
        ),
        now=now,
    )
    non_mfa_state = policy.start(
        verifier.verify(
            _token(signing_key, profile, now=now, claims={"amr": ["pwd"]}),
            expected_nonce=NONCE,
            now=now,
        ),
        now=now,
    )

    policy.require_privileged_mfa(mfa_state, now=now + timedelta(minutes=4))
    with pytest.raises(OidcValidationError, match="recent MFA required"):
        policy.require_privileged_mfa(mfa_state, now=now + timedelta(minutes=6))
    with pytest.raises(OidcValidationError, match="recent MFA required"):
        policy.require_privileged_mfa(non_mfa_state, now=now)


def test_profiles_nonce_and_naive_timestamps_are_bounded(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        OidcProviderProfile(
            issuer="http://idp.example",
            client_id="client",
            mfa_acr_values=frozenset({"mfa"}),
        )
    with pytest.raises(ValueError, match="MFA ACR"):
        OidcProviderProfile(
            issuer="https://idp.example",
            client_id="client",
            mfa_acr_values=frozenset(),
        )
    with pytest.raises(ValueError, match="nonce"):
        _verifier(signing_key, profile).verify(
            _token(signing_key, profile),
            expected_nonce="short",
        )
    principal = _verifier(signing_key, profile).verify(
        _token(signing_key, profile),
        expected_nonce=NONCE,
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        HardenedSessionPolicy().start(principal, now=datetime(2026, 1, 1))


def test_logout_is_idempotent(
    signing_key: JwtSigningKey,
    profile: OidcProviderProfile,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, profile).verify(
        _token(signing_key, profile, now=now),
        expected_nonce=NONCE,
        now=now,
    )
    policy = HardenedSessionPolicy()
    state = policy.start(principal, now=now)
    logged_out = policy.logout(state, now=now + timedelta(seconds=1))

    assert policy.logout(logged_out, now=now + timedelta(seconds=2)) is logged_out
