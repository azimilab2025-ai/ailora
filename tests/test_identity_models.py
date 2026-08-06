"""
AILORA P2-01: Identity Domain Model Contract Tests.

Validates Tenant, User, Membership, and RoleEnum models for:
- Correct attribute definitions and types
- Unique constraints and relationships
- No plaintext password storage
- Tenant isolation requirements
- Migration script existence and structure

These tests are structural and do not require a live database.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from sqlalchemy import inspect as sa_inspect

from ailora.domain.identity.models import (
    Membership,
    RoleEnum,
    Tenant,
    User,
)

REPO_ROOT = Path(__file__).parent.parent
IDENTITY_MIGRATION = REPO_ROOT / "alembic" / "versions" / "0002_identity.py"


# ─── RoleEnum ─────────────────────────────────────────────────────────────────


def test_role_enum_values() -> None:
    """RoleEnum must define owner, admin, member, viewer."""
    values = {r.value for r in RoleEnum}
    assert {"owner", "admin", "member", "viewer"} == values


# ─── Tenant model ─────────────────────────────────────────────────────────────


def test_tenant_table_name() -> None:
    assert Tenant.__tablename__ == "tenants"


def test_tenant_has_id_column() -> None:
    cols = {c.name for c in Tenant.__table__.columns}
    assert "id" in cols


def test_tenant_has_slug_column() -> None:
    col = Tenant.__table__.columns["slug"]
    assert col.unique or any(
        "slug" in str(idx.columns) for idx in Tenant.__table__.indexes if idx.unique
    )


def test_tenant_has_required_columns() -> None:
    cols = {c.name for c in Tenant.__table__.columns}
    required = {"id", "slug", "display_name", "is_active", "created_at"}
    assert required.issubset(cols), f"Missing columns: {required - cols}"


def test_tenant_is_active_default_true() -> None:
    col = Tenant.__table__.columns["is_active"]
    assert col.default is not None or col.server_default is not None


def test_tenant_has_memberships_relationship() -> None:
    mapper = sa_inspect(Tenant)
    rel_names = {r.key for r in mapper.relationships}
    assert "memberships" in rel_names


# ─── User model ───────────────────────────────────────────────────────────────


def test_user_table_name() -> None:
    assert User.__tablename__ == "users"


def test_user_has_required_columns() -> None:
    cols = {c.name for c in User.__table__.columns}
    required = {"id", "email", "hashed_password", "is_active", "is_superuser", "created_at"}
    assert required.issubset(cols)


def test_user_email_is_unique() -> None:
    col = User.__table__.columns["email"]
    assert col.unique or any(
        "email" in str(idx.columns) for idx in User.__table__.indexes if idx.unique
    )


def test_user_no_plaintext_password_column() -> None:
    """Users must store a hashed password, not a plaintext one."""
    col_names = {c.name for c in User.__table__.columns}
    assert "password" not in col_names, (
        "User must not have a 'password' column — use 'hashed_password'"
    )
    assert "hashed_password" in col_names


def test_user_has_memberships_relationship() -> None:
    mapper = sa_inspect(User)
    rel_names = {r.key for r in mapper.relationships}
    assert "memberships" in rel_names


# ─── Membership model ─────────────────────────────────────────────────────────


def test_membership_table_name() -> None:
    assert Membership.__tablename__ == "memberships"


def test_membership_has_required_columns() -> None:
    cols = {c.name for c in Membership.__table__.columns}
    required = {"id", "user_id", "tenant_id", "role", "is_active", "created_at"}
    assert required.issubset(cols)


def test_membership_unique_constraint_user_tenant() -> None:
    """Membership must enforce (user_id, tenant_id) uniqueness."""
    constraints = {c.name for c in Membership.__table__.constraints}
    assert "uq_membership_user_tenant" in constraints, (
        "Membership must have uq_membership_user_tenant unique constraint"
    )


def test_membership_has_user_relationship() -> None:
    mapper = sa_inspect(Membership)
    rel_names = {r.key for r in mapper.relationships}
    assert "user" in rel_names


def test_membership_has_tenant_relationship() -> None:
    mapper = sa_inspect(Membership)
    rel_names = {r.key for r in mapper.relationships}
    assert "tenant" in rel_names


# ─── Tenant isolation design contract ────────────────────────────────────────


def test_membership_tenant_id_has_foreign_key() -> None:
    """tenant_id must have a foreign key to tenants.id."""
    col = Membership.__table__.columns["tenant_id"]
    fk_targets = {fk.target_fullname for fk in col.foreign_keys}
    assert "tenants.id" in fk_targets, "membership.tenant_id must reference tenants.id"


def test_membership_user_id_has_foreign_key() -> None:
    """user_id must have a foreign key to users.id."""
    col = Membership.__table__.columns["user_id"]
    fk_targets = {fk.target_fullname for fk in col.foreign_keys}
    assert "users.id" in fk_targets, "membership.user_id must reference users.id"


# ─── UUID primary keys ───────────────────────────────────────────────────────


@pytest.mark.parametrize("model", [Tenant, User, Membership])
def test_model_pk_is_uuid(model: type[Tenant] | type[User] | type[Membership]) -> None:
    """All identity models must use UUID primary keys."""
    pk_cols = [c for c in model.__table__.columns if c.primary_key]
    assert pk_cols, f"{model.__name__} must have a primary key"
    # UUID columns have type name starting with UUID
    assert any("uuid" in str(c.type).lower() for c in pk_cols), (
        f"{model.__name__} primary key must be UUID type"
    )


# ─── Instance construction ────────────────────────────────────────────────────


def test_tenant_instantiation() -> None:
    t = Tenant(id=uuid.uuid4(), slug="test-tenant", display_name="Test Tenant")
    assert t.slug == "test-tenant"


def test_user_instantiation() -> None:
    u = User(id=uuid.uuid4(), email="test@ailora.local", hashed_password="$2b$hashed")
    assert u.email == "test@ailora.local"
    assert u.hashed_password.startswith("$2b$") or len(u.hashed_password) > 0


def test_membership_instantiation() -> None:
    uid = uuid.uuid4()
    tid = uuid.uuid4()
    m = Membership(id=uuid.uuid4(), user_id=uid, tenant_id=tid, role=RoleEnum.MEMBER)
    assert m.user_id == uid
    assert m.tenant_id == tid
    assert m.role == "member"


# ─── Migration file ───────────────────────────────────────────────────────────


def test_identity_migration_exists() -> None:
    """0002_identity.py migration must exist."""
    assert IDENTITY_MIGRATION.exists(), "alembic/versions/0002_identity.py not found"


def test_identity_migration_has_correct_down_revision() -> None:
    """Identity migration must chain from 0001_baseline."""
    text = IDENTITY_MIGRATION.read_text(encoding="utf-8")
    assert "0001_baseline" in text, "0002_identity.py must set down_revision = '0001_baseline'"


def test_identity_migration_creates_all_three_tables() -> None:
    """Migration must create tenants, users, and memberships tables."""
    text = IDENTITY_MIGRATION.read_text(encoding="utf-8")
    for table in ("tenants", "users", "memberships"):
        assert table in text, f"Migration must create '{table}' table"
