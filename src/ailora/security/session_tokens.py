"""High-entropy opaque refresh-token generation and digest contracts."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

_REFRESH_TOKEN_BYTES = 48
_REFRESH_TOKEN_TTL = timedelta(days=7)


@dataclass(frozen=True, slots=True)
class IssuedRefreshToken:
    """One-time plaintext delivery plus the digest persisted by the server."""

    plaintext: str
    digest: str
    expires_at: datetime


def hash_refresh_token(token: str) -> str:
    """Hash a high-entropy opaque token for storage and lookup."""
    if not token or len(token) < 32:
        raise ValueError("refresh token is malformed")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issue_refresh_token(*, now: datetime | None = None) -> IssuedRefreshToken:
    """Issue a refresh token whose plaintext is returned exactly once."""
    issued_at = now or datetime.now(UTC)
    plaintext = secrets.token_urlsafe(_REFRESH_TOKEN_BYTES)
    return IssuedRefreshToken(
        plaintext=plaintext,
        digest=hash_refresh_token(plaintext),
        expires_at=issued_at + _REFRESH_TOKEN_TTL,
    )
