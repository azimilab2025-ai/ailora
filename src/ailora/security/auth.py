"""
AILORA JWT authentication utilities.

Implements stateless JWT-based authentication per Prompt 15 §13.

Security contracts:
- Tokens are signed with HS256 using a secret resolved from environment only.
- Token expiry is enforced; expired tokens are rejected.
- No credential is ever logged, added to span attributes, or included in error bodies.
- Authentication proves identity only; authorization decisions are separate.
- The secret_key must be changed before any non-local deployment.
- Invalid/expired tokens always return HTTP 401, never HTTP 403 (to avoid oracle).

Note on bcrypt:
  passlib 1.7.4 is not compatible with bcrypt ≥ 4.1 due to an __about__ API change.
  We call the bcrypt library directly to avoid this incompatibility while keeping
  the bcrypt algorithm.  This is a stable, documented pattern.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from ailora.config import settings

# ---------------------------------------------------------------------------
# Password hashing (bcrypt direct — bypasses passlib/bcrypt version mismatch)
# ---------------------------------------------------------------------------

_BCRYPT_ROUNDS = 12


def hash_password(plaintext: str) -> str:
    """Return a bcrypt hash of the plaintext password."""
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    return bcrypt.hashpw(plaintext.encode("utf-8"), salt).decode("utf-8")


def verify_password(plaintext: str, hashed: str) -> bool:
    """Return True if plaintext matches the stored bcrypt hash."""
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))


# ---------------------------------------------------------------------------
# JWT token creation
# ---------------------------------------------------------------------------


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject:      Token subject (user UUID as string).
        extra_claims: Optional additional claims (e.g. tenant_id).

    Returns:
        Encoded JWT string.
    """
    now = datetime.now(tz=UTC)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        **(extra_claims or {}),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# JWT token decoding
# ---------------------------------------------------------------------------


class TokenError(Exception):
    """Raised when a JWT token is invalid, expired, or structurally wrong."""


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Args:
        token: The raw JWT string from the Authorization header.

    Returns:
        The validated token payload dict.

    Raises:
        TokenError: If the token is invalid, expired, or structurally wrong.
    """
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except JWTError as exc:
        raise TokenError("Invalid or expired token") from exc

    subject = payload.get("sub")
    if not subject:
        raise TokenError("Token missing subject claim")

    return payload
