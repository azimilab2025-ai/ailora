"""Provider-neutral OIDC ID-token verification and hardened session policy."""

from __future__ import annotations

import re
import secrets
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Any, Final
from urllib.parse import urlsplit
from uuid import UUID, uuid4

import jwt
from jwt.algorithms import RSAAlgorithm

_ALGORITHM: Final = "RS256"
_KID_PATTERN: Final = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_PRIVATE_JWK_FIELDS: Final = frozenset({"d", "p", "q", "dp", "dq", "qi", "oth"})
_MFA_METHODS: Final = frozenset({"mfa", "otp", "hwk"})
_REQUIRED_ID_TOKEN_CLAIMS: Final = (
    "aud",
    "auth_time",
    "exp",
    "iat",
    "iss",
    "nonce",
    "sid",
    "sub",
)


class OidcValidationError(Exception):
    """Generic fail-closed OIDC or session validation error."""


@dataclass(frozen=True, slots=True)
class OidcProviderProfile:
    """Pinned provider identity and bounded ID-token acceptance profile."""

    issuer: str
    client_id: str
    mfa_acr_values: frozenset[str]
    maximum_id_token_age: timedelta = timedelta(minutes=5)
    clock_skew: timedelta = timedelta(seconds=30)

    def __post_init__(self) -> None:
        issuer = self.issuer.strip().rstrip("/")
        parsed = urlsplit(issuer)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("OIDC issuer must be an explicit credential-free HTTPS URL")
        if not self.client_id.strip() or len(self.client_id) > 256:
            raise ValueError("OIDC client identifier must be explicit and bounded")
        if not self.mfa_acr_values or any(not value.strip() for value in self.mfa_acr_values):
            raise ValueError("at least one explicit MFA ACR value is required")
        if not timedelta(seconds=1) <= self.maximum_id_token_age <= timedelta(minutes=15):
            raise ValueError("maximum ID-token age must be between one second and fifteen minutes")
        if not timedelta(0) <= self.clock_skew <= timedelta(seconds=60):
            raise ValueError("clock skew must be between zero and sixty seconds")
        object.__setattr__(self, "issuer", issuer)
        object.__setattr__(self, "client_id", self.client_id.strip())
        object.__setattr__(
            self,
            "mfa_acr_values",
            frozenset(value.strip() for value in self.mfa_acr_values),
        )


@dataclass(frozen=True, slots=True)
class OidcPrincipal:
    """Verified external identity without tenant authorization authority."""

    issuer: str
    subject: str
    provider_session_id: str
    issued_at: datetime
    authenticated_at: datetime
    expires_at: datetime
    mfa_authenticated: bool
    acr: str | None
    amr: tuple[str, ...]
    verified_email: str | None


class OidcIdTokenVerifier:
    """Offline verifier using an injected, public-only, bounded JWKS snapshot."""

    def __init__(self, *, profile: OidcProviderProfile, jwks: Mapping[str, Any]) -> None:
        records = jwks.get("keys")
        if not isinstance(records, list) or not 1 <= len(records) <= 8:
            raise ValueError("OIDC JWKS must contain between one and eight keys")
        keys: dict[str, Any] = {}
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("OIDC JWK record must be an object")
            kid = record.get("kid")
            if not isinstance(kid, str) or not _KID_PATTERN.fullmatch(kid):
                raise ValueError("OIDC JWK kid is missing or unsafe")
            if kid in keys:
                raise ValueError("OIDC JWK identifiers must be unique")
            if _PRIVATE_JWK_FIELDS.intersection(record):
                raise ValueError("OIDC JWKS must never contain private key material")
            if (
                record.get("kty") != "RSA"
                or record.get("alg") != _ALGORITHM
                or record.get("use") != "sig"
            ):
                raise ValueError("OIDC JWK must be an RS256 signature key")
            try:
                keys[kid] = RSAAlgorithm.from_jwk(record)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError("OIDC JWK is malformed") from exc
        self._profile = profile
        self._keys = keys

    def verify(
        self,
        token: str,
        *,
        expected_nonce: str,
        now: datetime | None = None,
    ) -> OidcPrincipal:
        """Verify signature, provider binding, nonce, freshness, session, and MFA evidence."""
        if not 16 <= len(expected_nonce) <= 512:
            raise ValueError("OIDC nonce must be between sixteen and 512 characters")
        verification_time = _aware(now or datetime.now(UTC))
        try:
            header = jwt.get_unverified_header(token)
            if (
                header.get("alg") != _ALGORITHM
                or header.get("typ") != "JWT"
                or not isinstance(header.get("kid"), str)
                or "jku" in header
                or "x5u" in header
            ):
                raise OidcValidationError("OIDC validation failed")
            key = self._keys.get(header["kid"])
            if key is None:
                raise OidcValidationError("OIDC validation failed")
            payload: dict[str, Any] = jwt.decode(
                token,
                key,
                algorithms=[_ALGORITHM],
                audience=self._profile.client_id,
                issuer=self._profile.issuer,
                leeway=self._profile.clock_skew.total_seconds(),
                options={"require": list(_REQUIRED_ID_TOKEN_CLAIMS)},
            )
            nonce = payload.get("nonce")
            if not isinstance(nonce, str) or not secrets.compare_digest(nonce, expected_nonce):
                raise OidcValidationError("OIDC validation failed")
            self._validate_authorized_party(payload)
            issued_at = _numeric_date(payload, "iat")
            authenticated_at = _numeric_date(payload, "auth_time")
            expires_at = _numeric_date(payload, "exp")
            if verification_time - issued_at > self._profile.maximum_id_token_age:
                raise OidcValidationError("OIDC validation failed")
            if authenticated_at > verification_time + self._profile.clock_skew:
                raise OidcValidationError("OIDC validation failed")
            subject = payload.get("sub")
            provider_session_id = payload.get("sid")
            if not isinstance(subject, str) or not subject.strip():
                raise OidcValidationError("OIDC validation failed")
            if not isinstance(provider_session_id, str) or not provider_session_id.strip():
                raise OidcValidationError("OIDC validation failed")
            acr = payload.get("acr") if isinstance(payload.get("acr"), str) else None
            amr_value = payload.get("amr", [])
            if not isinstance(amr_value, list) or not all(
                isinstance(method, str) for method in amr_value
            ):
                raise OidcValidationError("OIDC validation failed")
            amr = tuple(sorted(set(amr_value)))
            mfa_authenticated = bool(
                acr in self._profile.mfa_acr_values and _MFA_METHODS.intersection(amr)
            )
            verified_email = _verified_email(payload)
            return OidcPrincipal(
                issuer=self._profile.issuer,
                subject=subject.strip(),
                provider_session_id=provider_session_id.strip(),
                issued_at=issued_at,
                authenticated_at=authenticated_at,
                expires_at=expires_at,
                mfa_authenticated=mfa_authenticated,
                acr=acr,
                amr=amr,
                verified_email=verified_email,
            )
        except OidcValidationError:
            raise
        except (KeyError, TypeError, ValueError, jwt.InvalidTokenError) as exc:
            raise OidcValidationError("OIDC validation failed") from exc

    def _validate_authorized_party(self, payload: Mapping[str, Any]) -> None:
        audience = payload.get("aud")
        if isinstance(audience, list) and len(audience) > 1:
            if payload.get("azp") != self._profile.client_id:
                raise OidcValidationError("OIDC validation failed")


@dataclass(frozen=True, slots=True)
class HardenedSessionState:
    """Immutable refresh-family state used to detect replay and enforce expiry."""

    session_id: UUID
    refresh_family_id: UUID
    issuer: str
    subject: str
    provider_session_id: str
    created_at: datetime
    last_rotated_at: datetime
    absolute_expires_at: datetime
    rotation_counter: int
    mfa_authenticated_at: datetime | None
    revoked_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class HardenedSessionPolicy:
    """Absolute, idle, rotation-replay, logout, and privileged-MFA controls."""

    absolute_lifetime: timedelta = timedelta(hours=8)
    idle_timeout: timedelta = timedelta(minutes=30)
    privileged_mfa_max_age: timedelta = timedelta(minutes=5)

    def __post_init__(self) -> None:
        if not timedelta(minutes=5) <= self.absolute_lifetime <= timedelta(hours=24):
            raise ValueError("absolute session lifetime must be between five minutes and one day")
        if not timedelta(minutes=1) <= self.idle_timeout <= self.absolute_lifetime:
            raise ValueError("idle timeout must be bounded by absolute lifetime")
        if not timedelta(seconds=1) <= self.privileged_mfa_max_age <= timedelta(minutes=15):
            raise ValueError("privileged MFA age must be between one second and fifteen minutes")

    def start(
        self,
        principal: OidcPrincipal,
        *,
        now: datetime | None = None,
    ) -> HardenedSessionState:
        """Start a server-side session from a verified OIDC principal."""
        started_at = _aware(now or datetime.now(UTC))
        if principal.expires_at <= started_at:
            raise OidcValidationError("session validation failed")
        return HardenedSessionState(
            session_id=uuid4(),
            refresh_family_id=uuid4(),
            issuer=principal.issuer,
            subject=principal.subject,
            provider_session_id=principal.provider_session_id,
            created_at=started_at,
            last_rotated_at=started_at,
            absolute_expires_at=started_at + self.absolute_lifetime,
            rotation_counter=0,
            mfa_authenticated_at=(
                principal.authenticated_at if principal.mfa_authenticated else None
            ),
        )

    def rotate(
        self,
        state: HardenedSessionState,
        *,
        presented_family_id: UUID,
        presented_rotation_counter: int,
        now: datetime | None = None,
    ) -> HardenedSessionState:
        """Rotate once; stale counters and wrong families are replay failures."""
        rotated_at = _aware(now or datetime.now(UTC))
        self._require_active(state, now=rotated_at)
        family_matches = secrets.compare_digest(
            str(state.refresh_family_id),
            str(presented_family_id),
        )
        if not family_matches or presented_rotation_counter != state.rotation_counter:
            raise OidcValidationError("session validation failed")
        return replace(
            state,
            rotation_counter=state.rotation_counter + 1,
            last_rotated_at=rotated_at,
        )

    def require_privileged_mfa(
        self,
        state: HardenedSessionState,
        *,
        now: datetime | None = None,
    ) -> None:
        """Require recent verified MFA for a privileged effect."""
        checked_at = _aware(now or datetime.now(UTC))
        self._require_active(state, now=checked_at)
        mfa_at = state.mfa_authenticated_at
        if (
            mfa_at is None
            or mfa_at > checked_at
            or checked_at - mfa_at > self.privileged_mfa_max_age
        ):
            raise OidcValidationError("recent MFA required")

    def logout(
        self,
        state: HardenedSessionState,
        *,
        now: datetime | None = None,
    ) -> HardenedSessionState:
        """Idempotently mark a session revoked."""
        if state.revoked_at is not None:
            return state
        return replace(state, revoked_at=_aware(now or datetime.now(UTC)))

    def _require_active(self, state: HardenedSessionState, *, now: datetime) -> None:
        if (
            state.revoked_at is not None
            or now >= state.absolute_expires_at
            or now - state.last_rotated_at > self.idle_timeout
        ):
            raise OidcValidationError("session validation failed")


def _numeric_date(payload: Mapping[str, Any], claim: str) -> datetime:
    value = payload.get(claim)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise OidcValidationError("OIDC validation failed")
    return datetime.fromtimestamp(value, tz=UTC)


def _verified_email(payload: Mapping[str, Any]) -> str | None:
    email = payload.get("email")
    if payload.get("email_verified") is not True or not isinstance(email, str):
        return None
    normalized = email.strip().casefold()
    return normalized if "@" in normalized and len(normalized) <= 320 else None


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("security timestamps must be timezone-aware")
    return value.astimezone(UTC)
