"""Fail-closed asymmetric access-token and public JWKS foundation."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any, Final, Literal
from urllib.parse import urlsplit
from uuid import UUID, uuid4

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from jwt.algorithms import RSAAlgorithm

_ALGORITHM: Final = "RS256"
_KID_PATTERN: Final = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_MINIMUM_RSA_BITS: Final = 2048
_RESERVED_CLAIMS: Final = frozenset({"aud", "exp", "iat", "iss", "jti", "nbf", "sub"})


class AsymmetricTokenError(Exception):
    """Safe generic error for invalid keys, profiles, or tokens."""


@dataclass(frozen=True, slots=True)
class AsymmetricTokenProfile:
    """Exact issuer, audience, lifetime, and algorithm verification profile."""

    issuer: str
    audience: str
    access_token_ttl: timedelta = timedelta(minutes=15)
    algorithm: Literal["RS256"] = "RS256"

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
            raise ValueError("issuer must be an explicit credential-free HTTPS URL")
        if not self.audience.strip():
            raise ValueError("audience must be explicit and non-empty")
        if not timedelta(seconds=1) <= self.access_token_ttl <= timedelta(hours=1):
            raise ValueError("access token lifetime must be between one second and one hour")
        object.__setattr__(self, "issuer", issuer)
        object.__setattr__(self, "audience", self.audience.strip())


@dataclass(frozen=True, slots=True)
class JwtSigningKey:
    """Validated RSA key record; private material is optional and never serialized."""

    kid: str
    public_key_pem: str
    private_key_pem: str | None = field(default=None, repr=False)

    @classmethod
    def from_private_pem(cls, *, kid: str, private_key_pem: str) -> JwtSigningKey:
        """Validate protected input material and derive the matching public key."""
        _validate_kid(kid)
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode("ascii"),
                password=None,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("private key is not valid unencrypted PEM") from exc
        if not isinstance(private_key, RSAPrivateKey):
            raise ValueError("private key must use RSA")
        if private_key.key_size < _MINIMUM_RSA_BITS:
            raise ValueError("RSA private key must be at least 2048 bits")
        public_pem = private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return cls(
            kid=kid,
            public_key_pem=public_pem.decode("ascii"),
            private_key_pem=private_key_pem,
        )

    def verification_only(self) -> JwtSigningKey:
        """Remove signing authority while retaining verification capability."""
        return JwtSigningKey(kid=self.kid, public_key_pem=self.public_key_pem)


class RotatingJwtKeyRing:
    """One active signer plus a bounded set of public verification keys."""

    def __init__(self, *, keys: Iterable[JwtSigningKey], active_kid: str) -> None:
        key_records = tuple(keys)
        by_kid = {key.kid: key for key in key_records}
        if not key_records:
            raise ValueError("key ring must not be empty")
        if len(by_kid) != len(key_records):
            raise ValueError("key identifiers must be unique")
        active = by_kid.get(active_kid)
        if active is None or active.private_key_pem is None:
            raise ValueError("active key must exist and contain private signing material")
        if len(key_records) > 8:
            raise ValueError("key ring exceeds the bounded eight-key verification window")
        for key in key_records:
            _validate_public_key(key)
        self._keys = by_kid
        self._active_kid = active_kid

    @property
    def active_signing_key(self) -> JwtSigningKey:
        """Return the configured active signer."""
        return self._keys[self._active_kid]

    def resolve_verification_key(self, kid: str) -> JwtSigningKey:
        """Resolve an allowlisted key identifier without network retrieval."""
        key = self._keys.get(kid)
        if key is None:
            raise AsymmetricTokenError("token validation failed")
        return key

    def rotate(self, new_active_key: JwtSigningKey) -> RotatingJwtKeyRing:
        """Promote a new signer and retain public-only forms of previous keys."""
        if new_active_key.kid in self._keys:
            raise ValueError("rotation requires a new key identifier")
        retained = [key.verification_only() for key in self._keys.values()]
        return RotatingJwtKeyRing(
            keys=[*retained, new_active_key],
            active_kid=new_active_key.kid,
        )

    def public_jwks(self) -> dict[str, list[dict[str, Any]]]:
        """Return deterministic public-only JWKS records sorted by key identifier."""
        records: list[dict[str, Any]] = []
        for kid in sorted(self._keys):
            public_key = _load_public_key(self._keys[kid])
            jwk = dict(RSAAlgorithm.to_jwk(public_key, as_dict=True))
            jwk.update({"alg": _ALGORITHM, "kid": kid, "use": "sig"})
            records.append(jwk)
        return {"keys": records}


def issue_access_token(
    *,
    subject: str,
    key_ring: RotatingJwtKeyRing,
    profile: AsymmetricTokenProfile,
    extra_claims: Mapping[str, Any] | None = None,
    now: datetime | None = None,
    jti: UUID | None = None,
) -> str:
    """Issue a short-lived RS256 token with mandatory identity and replay claims."""
    if not subject.strip():
        raise ValueError("subject must be explicit and non-empty")
    supplied_claims = dict(extra_claims or {})
    overlap = _RESERVED_CLAIMS.intersection(supplied_claims)
    if overlap:
        raise ValueError(f"reserved claims cannot be overridden: {','.join(sorted(overlap))}")
    issued_at = now or datetime.now(UTC)
    if issued_at.tzinfo is None or issued_at.utcoffset() is None:
        raise ValueError("token time must be timezone-aware")
    key = key_ring.active_signing_key
    private_key_pem = key.private_key_pem
    if private_key_pem is None:
        raise AsymmetricTokenError("active signing key is unavailable")
    payload: dict[str, Any] = {
        "aud": profile.audience,
        "exp": issued_at + profile.access_token_ttl,
        "iat": issued_at,
        "iss": profile.issuer,
        "jti": str(jti or uuid4()),
        "nbf": issued_at,
        "sub": subject.strip(),
        **supplied_claims,
    }
    return jwt.encode(
        payload,
        private_key_pem,
        algorithm=profile.algorithm,
        headers={"alg": profile.algorithm, "kid": key.kid, "typ": "JWT"},
    )


def decode_access_token(
    token: str,
    *,
    key_ring: RotatingJwtKeyRing,
    profile: AsymmetricTokenProfile,
    leeway_seconds: int = 0,
) -> dict[str, Any]:
    """Validate exact header, key, signature, issuer, audience, time, and JTI."""
    if not 0 <= leeway_seconds <= 30:
        raise ValueError("verification leeway must be between zero and thirty seconds")
    try:
        header = jwt.get_unverified_header(token)
        if (
            header.get("alg") != profile.algorithm
            or header.get("typ") != "JWT"
            or not isinstance(header.get("kid"), str)
        ):
            raise AsymmetricTokenError("token validation failed")
        key = key_ring.resolve_verification_key(header["kid"])
        payload: dict[str, Any] = jwt.decode(
            token,
            key.public_key_pem,
            algorithms=[profile.algorithm],
            audience=profile.audience,
            issuer=profile.issuer,
            leeway=leeway_seconds,
            options={"require": sorted(_RESERVED_CLAIMS)},
        )
        if not isinstance(payload.get("sub"), str) or not payload["sub"].strip():
            raise AsymmetricTokenError("token validation failed")
        token_id = payload.get("jti")
        if not isinstance(token_id, str) or str(UUID(token_id)) != token_id:
            raise AsymmetricTokenError("token validation failed")
        return payload
    except AsymmetricTokenError:
        raise
    except (KeyError, TypeError, ValueError, jwt.InvalidTokenError) as exc:
        raise AsymmetricTokenError("token validation failed") from exc


def _validate_kid(kid: str) -> None:
    if not _KID_PATTERN.fullmatch(kid):
        raise ValueError("key identifier contains forbidden characters or length")


def _load_public_key(key: JwtSigningKey) -> RSAPublicKey:
    try:
        public_key = serialization.load_pem_public_key(key.public_key_pem.encode("ascii"))
    except (TypeError, ValueError) as exc:
        raise ValueError("public key is not valid PEM") from exc
    if not isinstance(public_key, RSAPublicKey):
        raise ValueError("public key must use RSA")
    if public_key.key_size < _MINIMUM_RSA_BITS:
        raise ValueError("RSA public key must be at least 2048 bits")
    return public_key


def _validate_public_key(key: JwtSigningKey) -> None:
    _validate_kid(key.kid)
    _load_public_key(key)
