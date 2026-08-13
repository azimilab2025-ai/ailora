"""Identity API and refresh-session lifecycle contracts."""

from __future__ import annotations

import importlib
from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def _tokens() -> object:
    return importlib.import_module("ailora.security.session_tokens")


def _repository_module() -> object:
    return importlib.import_module("ailora.domain.identity.session_repository")


@pytest.fixture
async def database() -> AsyncGenerator[AsyncSession, None]:
    from ailora.db.base import Base

    importlib.import_module("ailora.domain.identity.models")
    importlib.import_module("ailora.domain.identity.session_models")

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session

    await engine.dispose()


def test_refresh_token_is_high_entropy_and_hash_only() -> None:
    tokens = _tokens()
    issued = tokens.issue_refresh_token()

    assert len(issued.plaintext) >= 64
    assert len(issued.digest) == 64
    assert issued.plaintext != issued.digest
    assert tokens.hash_refresh_token(issued.plaintext) == issued.digest


def test_short_refresh_token_is_rejected() -> None:
    tokens = _tokens()
    with pytest.raises(ValueError, match="malformed"):
        tokens.hash_refresh_token("too-short")


@pytest.mark.asyncio
async def test_session_persists_digest_never_plaintext(database: AsyncSession) -> None:
    tokens = _tokens()
    repository_module = _repository_module()
    issued = tokens.issue_refresh_token()
    user_id = uuid4()

    from ailora.domain.identity.models import User

    database.add(
        User(
            id=user_id,
            email="session-user@example.test",
            hashed_password="$2b$12$test-placeholder",
        )
    )
    await database.flush()

    repository = repository_module.IdentitySessionRepository(database)
    session = await repository.create(
        user_id=user_id,
        refresh_token_hash=issued.digest,
        expires_at=issued.expires_at,
    )

    assert session.refresh_token_hash == issued.digest
    assert session.refresh_token_hash != issued.plaintext


@pytest.mark.asyncio
async def test_revoked_session_cannot_be_reused(database: AsyncSession) -> None:
    tokens = _tokens()
    repository_module = _repository_module()
    now = datetime.now(UTC)
    issued = tokens.issue_refresh_token(now=now)
    user_id = uuid4()

    from ailora.domain.identity.models import User

    database.add(
        User(
            id=user_id,
            email="revoked-user@example.test",
            hashed_password="$2b$12$test-placeholder",
        )
    )
    await database.flush()

    repository = repository_module.IdentitySessionRepository(database)
    session = await repository.create(
        user_id=user_id,
        refresh_token_hash=issued.digest,
        expires_at=issued.expires_at,
    )
    await repository.revoke(session, now=now)

    assert (
        await repository.get_active_by_hash(
            refresh_token_hash=issued.digest,
            now=now,
        )
        is None
    )


@pytest.mark.asyncio
async def test_expired_session_cannot_be_used(database: AsyncSession) -> None:
    tokens = _tokens()
    repository_module = _repository_module()
    now = datetime.now(UTC)
    issued = tokens.issue_refresh_token(now=now - timedelta(days=8))
    user_id = uuid4()

    from ailora.domain.identity.models import User

    database.add(
        User(
            id=user_id,
            email="expired-user@example.test",
            hashed_password="$2b$12$test-placeholder",
        )
    )
    await database.flush()

    repository = repository_module.IdentitySessionRepository(database)
    await repository.create(
        user_id=user_id,
        refresh_token_hash=issued.digest,
        expires_at=issued.expires_at,
    )

    assert (
        await repository.get_active_by_hash(
            refresh_token_hash=issued.digest,
            now=now,
        )
        is None
    )


def test_openapi_exposes_complete_identity_session_lifecycle() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    paths = schema["paths"]

    assert "/v1/identity/login" in paths
    assert "/v1/identity/refresh" in paths
    assert "/v1/identity/logout" in paths
    assert "post" in paths["/v1/identity/login"]
    assert "post" in paths["/v1/identity/refresh"]
    assert "post" in paths["/v1/identity/logout"]


def test_token_response_never_contains_password_or_digest() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    response = schema["components"]["schemas"]["TokenPairResponse"]
    fields = set(response.get("properties", {}))

    assert fields == {"access_token", "refresh_token", "token_type"}
    assert "password" not in fields
    assert "refresh_token_hash" not in fields


def test_refresh_request_uses_secret_field() -> None:
    router_module = importlib.import_module("ailora.api.routers.identity_sessions")
    field = router_module.RefreshRequest.model_fields["refresh_token"]

    assert field.annotation.__name__ == "SecretStr"
