"""
AILORA P1-02: Database and Alembic Baseline Contract Tests.

Validates the structural requirements for the database infrastructure:
- Session factory module exists and is correctly typed.
- Alembic configuration exists and points to the correct schema.
- Initial migration script exists with the correct structure.
- No hardcoded secrets in any database configuration file.

These tests are structural and do not require a live database connection.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
ALEMBIC_INI = REPO_ROOT / "alembic.ini"
ALEMBIC_ENV = REPO_ROOT / "alembic" / "env.py"
ALEMBIC_VERSIONS = REPO_ROOT / "alembic" / "versions"
SESSION_MODULE = REPO_ROOT / "src" / "ailora" / "db" / "session.py"
BASE_MODULE = REPO_ROOT / "src" / "ailora" / "db" / "base.py"
DB_INIT = REPO_ROOT / "src" / "ailora" / "db" / "__init__.py"


# ─── Alembic configuration ────────────────────────────────────────────────────


def test_alembic_ini_exists() -> None:
    """alembic.ini must exist at the repository root."""
    assert ALEMBIC_INI.exists(), "alembic.ini not found at repository root"


def test_alembic_env_exists() -> None:
    """alembic/env.py must exist."""
    assert ALEMBIC_ENV.exists(), "alembic/env.py not found"


def test_alembic_versions_dir_exists() -> None:
    """alembic/versions/ directory must exist."""
    assert ALEMBIC_VERSIONS.is_dir(), "alembic/versions/ directory not found"


def test_alembic_env_uses_ailora_settings() -> None:
    """alembic/env.py must import from ailora.config to resolve database URL."""
    text = ALEMBIC_ENV.read_text(encoding="utf-8")
    assert "ailora.config" in text, "alembic/env.py must import settings from ailora.config"


def test_alembic_env_targets_base_metadata() -> None:
    """alembic/env.py must reference Base.metadata for autogenerate support."""
    text = ALEMBIC_ENV.read_text(encoding="utf-8")
    assert "Base.metadata" in text, "alembic/env.py must set target_metadata = Base.metadata"


def test_alembic_env_is_async() -> None:
    """alembic/env.py must use async engine (async_engine_from_config or equivalent)."""
    text = ALEMBIC_ENV.read_text(encoding="utf-8")
    assert "async" in text.lower(), "alembic/env.py must use async migration runner"


def test_alembic_ini_no_hardcoded_credentials() -> None:
    """alembic.ini must not contain hardcoded database credentials."""
    text = ALEMBIC_INI.read_text(encoding="utf-8")
    forbidden = ["password", "secret", "postgres://", "postgresql://"]
    for pattern in forbidden:
        assert pattern not in text.lower(), (
            f"alembic.ini must not contain hardcoded credential pattern: '{pattern}'"
        )


# ─── Initial migration ───────────────────────────────────────────────────────


def test_baseline_migration_exists() -> None:
    """At least one migration file must exist in alembic/versions/."""
    migration_files = list(ALEMBIC_VERSIONS.glob("*.py"))
    non_init = [f for f in migration_files if f.name != "__init__.py"]
    assert non_init, "No migration files found in alembic/versions/"


def test_baseline_migration_has_upgrade_and_downgrade() -> None:
    """Baseline migration must define upgrade() and downgrade() functions."""
    migration_files = [f for f in ALEMBIC_VERSIONS.glob("*.py") if f.name != "__init__.py"]
    assert migration_files, "No migration files found"
    # Check the earliest migration (sorted by name)
    first_migration = sorted(migration_files)[0]
    text = first_migration.read_text(encoding="utf-8")
    assert "def upgrade(" in text, f"{first_migration.name} must define upgrade()"
    assert "def downgrade(" in text, f"{first_migration.name} must define downgrade()"


def test_baseline_migration_has_revision_id() -> None:
    """Baseline migration must define a revision identifier."""
    migration_files = [f for f in ALEMBIC_VERSIONS.glob("*.py") if f.name != "__init__.py"]
    first_migration = sorted(migration_files)[0]
    text = first_migration.read_text(encoding="utf-8")
    assert "revision" in text, f"{first_migration.name} must define a revision ID"


# ─── Database session module ─────────────────────────────────────────────────


def test_db_session_module_exists() -> None:
    """src/ailora/db/session.py must exist."""
    assert SESSION_MODULE.exists(), "src/ailora/db/session.py not found"


def test_db_base_module_exists() -> None:
    """src/ailora/db/base.py must exist."""
    assert BASE_MODULE.exists(), "src/ailora/db/base.py not found"


def test_db_package_init_exists() -> None:
    """src/ailora/db/__init__.py must exist."""
    assert DB_INIT.exists(), "src/ailora/db/__init__.py not found"


def test_db_session_uses_async_session() -> None:
    """session.py must use AsyncSession (async-first architecture)."""
    text = SESSION_MODULE.read_text(encoding="utf-8")
    assert "AsyncSession" in text, "session.py must use SQLAlchemy AsyncSession"


def test_db_session_has_get_db_dependency() -> None:
    """session.py must define a get_db FastAPI dependency."""
    text = SESSION_MODULE.read_text(encoding="utf-8")
    assert "get_db" in text, "session.py must define get_db dependency"


def test_db_session_no_hardcoded_credentials() -> None:
    """session.py must not contain hardcoded database credentials."""
    text = SESSION_MODULE.read_text(encoding="utf-8")
    forbidden = ["password=", "PASSWORD=", "postgres://ailora:ailora"]
    for pattern in forbidden:
        assert pattern not in text, f"session.py must not contain hardcoded credential: '{pattern}'"


def test_db_base_has_declarative_base() -> None:
    """base.py must define a SQLAlchemy DeclarativeBase subclass."""
    text = BASE_MODULE.read_text(encoding="utf-8")
    assert "DeclarativeBase" in text, "base.py must define a class inheriting from DeclarativeBase"


# ─── Import sanity (no live connection required) ──────────────────────────────


@pytest.mark.asyncio
async def test_db_session_module_importable() -> None:
    """ailora.db.session must be importable without a live database connection."""
    # Import lazily to avoid engine creation at test collection time
    import importlib

    module = importlib.import_module("ailora.db.session")
    assert hasattr(module, "get_db"), "session module must export get_db"
    assert hasattr(module, "AsyncSessionLocal"), "session module must export AsyncSessionLocal"


@pytest.mark.asyncio
async def test_db_base_importable() -> None:
    """ailora.db.base must be importable and expose Base."""
    import importlib

    module = importlib.import_module("ailora.db.base")
    assert hasattr(module, "Base"), "db.base module must export Base"
