"""
AILORA database session factory.

Provides a SQLAlchemy async engine and session factory configured from
`ailora.config.settings`.  The readiness probe (PHASE_1) and all repository
layers use `get_db` as a FastAPI dependency.

Security: the database URL is resolved from the environment, never hardcoded.
Tenant isolation: callers are responsible for applying tenant filters — this
module only manages the connection lifecycle.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.config import settings

# --- Engine -------------------------------------------------------------------
# `echo=False` in production; never log queries containing secrets.
# `pool_pre_ping=True` detects stale connections before use.
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# --- Session factory ----------------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# --- FastAPI dependency -------------------------------------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session; close it on exit regardless of outcome."""
    async with AsyncSessionLocal() as session:
        yield session
