"""Tenant-scoped persistence model for advisory SSA scenarios."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from ailora.db.base import Base


class ScenarioRecord(Base):
    """Immutable-input snapshot; every query must include ``tenant_id``."""

    __tablename__ = "ssa_scenarios"
    __table_args__ = (
        Index("ix_ssa_scenarios_tenant_created", "tenant_id", "created_at"),
        CheckConstraint("advisory_only", name="ck_ssa_scenarios_advisory_only"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    reference_epoch: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    primary_object: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    secondary_object: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    combined_classification: Mapped[str] = mapped_column(String(32), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )
