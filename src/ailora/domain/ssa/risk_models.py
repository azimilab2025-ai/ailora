"""Tenant-scoped persistence for advisory SSA risk assessments."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from ailora.db.base import Base


class RiskAssessmentRecord(Base):
    """Persisted risk assessment constrained to tenant, scenario, and screening."""

    __tablename__ = "ssa_risk_assessments"
    __table_args__ = (
        Index(
            "ix_ssa_risk_tenant_scenario_screening_created",
            "tenant_id",
            "scenario_id",
            "screening_id",
            "created_at",
        ),
        CheckConstraint("advisory_only", name="ck_ssa_risk_advisory_only"),
        CheckConstraint("distance_km >= 0", name="ck_ssa_risk_nonnegative_distance"),
        CheckConstraint("threshold_km > 0", name="ck_ssa_risk_positive_threshold"),
        CheckConstraint(
            "risk_level IN ('NEGLIGIBLE', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL')",
            name="ck_ssa_risk_level_domain",
        ),
        CheckConstraint(
            "screening_outcome IN ('CONJUNCTION_POSSIBLE', 'NO_CONJUNCTION')",
            name="ck_ssa_risk_screening_outcome_domain",
        ),
        CheckConstraint(
            "screening_tier = 'T0_PHY_C1'",
            name="ck_ssa_risk_screening_tier_domain",
        ),
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
    screening_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_screenings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    threshold_km: Mapped[float] = mapped_column(Float, nullable=False)
    screening_outcome: Mapped[str] = mapped_column(String(64), nullable=False)
    screening_tier: Mapped[str] = mapped_column(String(32), nullable=False)
    combined_classification: Mapped[str] = mapped_column(String(32), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    provenance_label: Mapped[str] = mapped_column(Text, nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )
