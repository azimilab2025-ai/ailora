"""Managed asynchronous database engine and session lifecycle."""

import asyncio
from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ailora.config import settings
from ailora.db.tenant_context import (
    clear_session_context,
    configure_session_context,
    context_from_request,
)

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_timeout=settings.database_pool_timeout_seconds,
    pool_recycle=settings.database_pool_recycle_seconds,
    pool_use_lifo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def probe_database() -> bool:
    """Return whether the shared database engine answers a bounded read-only probe."""
    try:
        async with asyncio.timeout(settings.database_probe_timeout_seconds):
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        return False

    return True


async def close_database() -> None:
    """Dispose the shared engine during graceful application shutdown."""
    async with asyncio.timeout(settings.database_probe_timeout_seconds):
        await engine.dispose()


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-bound session and close it regardless of request outcome."""
    async with AsyncSessionLocal() as session:
        context = context_from_request(
            request,
            statement_timeout_ms=settings.database_statement_timeout_ms,
            lock_timeout_ms=settings.database_lock_timeout_ms,
            idle_transaction_timeout_ms=settings.database_idle_transaction_timeout_ms,
        )
        configure_session_context(session, context)
        try:
            yield session
        finally:
            clear_session_context(session)
