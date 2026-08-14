"""Tenant-scoped persistence model for advisory T0/PHY-C1 screenings."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from ailora.db.base import Base


class ScreeningRecord(Base):
    """Persisted advisory screening whose access is always tenant-filtered."""

    __tablename__ = "ssa_screenings"
    __table_args__ = (
        Index(
            "ix_ssa_screenings_tenant_scenario_created",
            "tenant_id",
            "scenario_id",
            "created_at",
        ),
        CheckConstraint("advisory_only", name="ck_ssa_screenings_advisory_only"),
        CheckConstraint("threshold_km > 0", name="ck_ssa_screenings_positive_threshold"),
        CheckConstraint("distance_km >= 0", name="ck_ssa_screenings_nonnegative_distance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    primary_state: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    secondary_state: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    threshold_km: Mapped[float] = mapped_column(Float, nullable=False)
    tier: Mapped[str] = mapped_column(String(32), nullable=False)
    outcome: Mapped[str] = mapped_column(String(64), nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    combined_classification: Mapped[str] = mapped_column(String(32), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    advisory_statement: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )
