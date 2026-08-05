"""
Alembic environment configuration for AILORA.

- Reads database URL from ailora.config.settings (environment variable AILORA_DATABASE_URL).
- Uses asyncpg-compatible URL with run_sync wrapper for async engine.
- target_metadata is set to Base.metadata so autogenerate works.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# -- Import AILORA models so their tables appear in metadata ------------------
from ailora.config import settings  # noqa: E402
from ailora.db.base import Base  # noqa: E402

# Models must be imported here so their mappers are registered on Base.metadata.
# Add each new model module below as it is created.
# from ailora.domain.identity.models import *  # noqa: F401, F403

# --- Alembic config ----------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url from AILORA settings so the .ini placeholder is unused.
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


# --- Offline mode ------------------------------------------------------------
def run_migrations_offline() -> None:
    """Generate SQL without a live connection (useful for review/audit)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# --- Online mode (async) -----------------------------------------------------
def do_run_migrations(connection: object) -> None:
    context.configure(
        connection=connection,  # type: ignore[arg-type]
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations within a sync wrapper."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# --- Entry point -------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
