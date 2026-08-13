"""Managed asynchronous database engine and session lifecycle."""

import asyncio
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ailora.config import settings

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


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a managed session and close it regardless of request outcome."""
    async with AsyncSessionLocal() as session:
        yield session
