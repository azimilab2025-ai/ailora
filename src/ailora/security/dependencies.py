"""
AILORA FastAPI authentication dependencies.

Provides reusable FastAPI dependencies for extracting and validating
JWT tokens from the Authorization: Bearer header.

Usage in route handlers::

    from ailora.security.dependencies import require_authenticated_user
    from fastapi import Depends

    @router.get("/protected")
    async def protected(token_data: dict = Depends(require_authenticated_user)):
        user_id = token_data["sub"]
        ...

Security rules:
- Dependencies raise HTTP 401 with a safe generic message on any failure.
- No token value or secret is included in error responses.
- Authentication dependencies do NOT perform authorization; callers must check
  tenant membership and role separately (Prompt 15 §13).
"""

from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ailora.security.auth import TokenError, decode_access_token

_bearer_scheme = HTTPBearer(auto_error=False)

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


async def require_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),  # noqa: B008
) -> dict[str, Any]:
    """
    FastAPI dependency: extract and validate the Bearer JWT token.

    Returns:
        Validated token payload dict (contains at minimum {"sub": user_id}).

    Raises:
        HTTPException 401: If no token, invalid token, or expired token.
    """
    if credentials is None:
        raise _UNAUTHORIZED
    try:
        payload = decode_access_token(credentials.credentials)
    except TokenError:
        raise _UNAUTHORIZED  # noqa: B904 — intentional: no chain exposure
    return payload
