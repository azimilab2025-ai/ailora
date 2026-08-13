"""Identity login, refresh rotation, and idempotent logout endpoints."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.identity.repositories import UserRepository
from ailora.domain.identity.session_repository import IdentitySessionRepository
from ailora.security.auth import create_access_token, verify_password
from ailora.security.session_tokens import hash_refresh_token, issue_refresh_token

router = APIRouter(prefix="/v1/identity", tags=["Identity"])


class LoginRequest(BaseModel):
    """Credentials accepted only over the deployment TLS boundary."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=320)
    password: SecretStr = Field(min_length=8, max_length=1024)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if "@" not in normalized:
            raise ValueError("email is invalid")
        return normalized


class RefreshRequest(BaseModel):
    """Opaque refresh credential used for rotation or revocation."""

    model_config = ConfigDict(extra="forbid")

    refresh_token: SecretStr = Field(min_length=32, max_length=512)


class TokenPairResponse(BaseModel):
    """Short-lived access token and rotating opaque refresh token."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105 - OAuth token type, not a credential


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _password_matches(plaintext: str, password_hash: str) -> bool:
    try:
        return verify_password(plaintext, password_hash)
    except (TypeError, ValueError):
        return False


@router.post(
    "/login",
    response_model=TokenPairResponse,
    summary="Authenticate and start a refresh session",
)
async def login(
    request: LoginRequest,
    database: Annotated[AsyncSession, Depends(get_db)],
) -> TokenPairResponse:
    user = await UserRepository(database).get_by_email(request.email)
    if (
        user is None
        or not user.is_active
        or not _password_matches(request.password.get_secret_value(), user.hashed_password)
    ):
        raise _unauthorized()

    refresh = issue_refresh_token()
    await IdentitySessionRepository(database).create(
        user_id=user.id,
        refresh_token_hash=refresh.digest,
        expires_at=refresh.expires_at,
    )
    await database.commit()

    return TokenPairResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=refresh.plaintext,
    )


@router.post(
    "/refresh",
    response_model=TokenPairResponse,
    summary="Rotate a valid refresh session",
)
async def refresh_session(
    request: RefreshRequest,
    database: Annotated[AsyncSession, Depends(get_db)],
) -> TokenPairResponse:
    now = datetime.now(UTC)
    repository = IdentitySessionRepository(database)
    digest = hash_refresh_token(request.refresh_token.get_secret_value())
    existing = await repository.get_active_by_hash(
        refresh_token_hash=digest,
        now=now,
        lock=True,
    )
    if existing is None:
        raise _unauthorized()

    user = await UserRepository(database).get_by_id(existing.user_id)
    if user is None or not user.is_active:
        await repository.revoke(existing, now=now)
        await database.commit()
        raise _unauthorized()

    rotated = issue_refresh_token(now=now)
    await repository.revoke(existing, now=now)
    await repository.create(
        user_id=user.id,
        refresh_token_hash=rotated.digest,
        expires_at=rotated.expires_at,
    )
    await database.commit()

    return TokenPairResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=rotated.plaintext,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Idempotently revoke a refresh session",
)
async def logout(
    request: RefreshRequest,
    database: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    now = datetime.now(UTC)
    repository = IdentitySessionRepository(database)
    digest = hash_refresh_token(request.refresh_token.get_secret_value())
    existing = await repository.get_active_by_hash(
        refresh_token_hash=digest,
        now=now,
        lock=True,
    )
    if existing is not None:
        await repository.revoke(existing, now=now)
        await database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
