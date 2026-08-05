"""
AILORA Identity and Access domain models.

Implements Prompt 15 §12 multi-tenancy with shared_database_with_tenant_key model.

Entity hierarchy:
  Tenant  1──* Membership  *──1  User
  Role    1──* Membership

Design rules:
- All tenant-scoped queries MUST filter by tenant_id.
- tenant_id is resolved from identity + membership, never from raw client input alone.
- Passwords are hashed; no plaintext passwords are ever stored or logged.
- Soft delete is not used by default (Prompt 15 §15 principle).
- Timestamps are stored in UTC (SQLAlchemy server_default=func.now() in UTC).
- No spacecraft command path exists in this module — permanently denied.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ailora.db.base import Base

# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------


class RoleEnum(StrEnum):
    """Built-in roles for tenant membership."""

    OWNER = "owner"       # Full access within the tenant
    ADMIN = "admin"       # Administrative access, cannot delete tenant
    MEMBER = "member"     # Standard access
    VIEWER = "viewer"     # Read-only access


# ---------------------------------------------------------------------------
# Tenant
# ---------------------------------------------------------------------------


class Tenant(Base):
    """
    A tenant (organisation / workspace) within the AILORA platform.

    All tenant-scoped data carries a foreign key to this table.
    Tenant context must be resolved from authenticated identity,
    not from arbitrary client-supplied values.
    """

    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
        comment="URL-safe unique identifier for the tenant",
    )
    display_name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        comment="Human-readable name",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Inactive tenants cannot authenticate",
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    memberships: Mapped[list[Membership]] = relationship(
        "Membership",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------


class User(Base):
    """
    A platform user (human operator or service account).

    Users exist at platform scope; tenant membership is through Membership.
    Passwords are stored as bcrypt hashes — never in plaintext.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
        comment="RFC 5321 email address — used as login identity",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        comment="bcrypt hash; plaintext password is never stored",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Inactive users cannot authenticate",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Platform-level superuser; tenant isolation still applies",
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    memberships: Mapped[list[Membership]] = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ---------------------------------------------------------------------------
# Membership
# ---------------------------------------------------------------------------


class Membership(Base):
    """
    A user's membership in a tenant, with an assigned role.

    This is the authoritative join table for tenant–user association.
    Tenant context is always derived from a Membership record validated
    against a trusted authentication token.

    Unique constraint: a user may have at most one active membership per tenant.
    """

    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", name="uq_membership_user_tenant"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=RoleEnum.MEMBER,
        comment="Role within this tenant (owner/admin/member/viewer)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Revoked memberships cannot grant access",
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship("User", back_populates="memberships")
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="memberships")
