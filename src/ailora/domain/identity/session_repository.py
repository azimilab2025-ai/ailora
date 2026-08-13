"""Database access for revocable identity refresh sessions."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.session_models import IdentitySession


class IdentitySessionRepository:
    """Persist and revoke refresh sessions without storing raw tokens."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> IdentitySession:
        identity_session = IdentitySession(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
        self._session.add(identity_session)
        await self._session.flush()
        return identity_session

    async def get_active_by_hash(
        self,
        *,
        refresh_token_hash: str,
        now: datetime,
        lock: bool = False,
    ) -> IdentitySession | None:
        statement = select(IdentitySession).where(
            IdentitySession.refresh_token_hash == refresh_token_hash,
            IdentitySession.revoked_at.is_(None),
            IdentitySession.expires_at > now,
        )
        if lock:
            statement = statement.with_for_update()
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def revoke(self, identity_session: IdentitySession, *, now: datetime) -> None:
        identity_session.revoked_at = now
        await self._session.flush()

    async def revoke_all_for_user(self, *, user_id: uuid.UUID, now: datetime) -> int:
        result = await self._session.execute(
            update(IdentitySession)
            .where(
                IdentitySession.user_id == user_id,
                IdentitySession.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )
        return int(getattr(result, "rowcount", 0) or 0)
