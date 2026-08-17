"""Append-only tenant-scoped persistence model for SSA audit evidence."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from ailora.db.base import Base

_EVENT_TYPES_SQL = (
    "'SCENARIO_INGESTED', 'SCENARIO_SCREENED', 'SCENARIO_RISK_ASSESSED', "
    "'REVIEW_OPENED', 'REVIEW_STATE_CHANGED', 'REVIEW_CLOSED', "
    "'USER_AUTHENTICATED', 'USER_AUTH_FAILED', 'ACCESS_GRANTED', 'ACCESS_DENIED'"
)


class AuditEventRecord(Base):
    """Immutable-by-contract audit row; repositories expose no mutation methods."""

    __tablename__ = "ssa_audit_events"
    __table_args__ = (
        Index("ix_ssa_audit_events_tenant_time", "tenant_id", "timestamp_utc", "id"),
        Index(
            "ix_ssa_audit_events_tenant_resource",
            "tenant_id",
            "resource_type",
            "resource_id",
        ),
        CheckConstraint(f"event_type IN ({_EVENT_TYPES_SQL})", name="ck_ssa_audit_event_type"),
        CheckConstraint(
            "length(resource_type) BETWEEN 1 AND 32", name="ck_ssa_audit_resource_type"
        ),
        CheckConstraint("length(outcome) BETWEEN 1 AND 32", name="ck_ssa_audit_outcome"),
        CheckConstraint("length(detail) <= 1000", name="ck_ssa_audit_detail_length"),
        CheckConstraint("advisory_only", name="ck_ssa_audit_advisory_only"),
        CheckConstraint("sequence_no > 0", name="ck_ssa_audit_sequence_positive"),
        CheckConstraint("length(previous_hash) = 64", name="ck_ssa_audit_previous_hash_length"),
        CheckConstraint("length(event_hash) = 64", name="ck_ssa_audit_event_hash_length"),
        Index("uq_ssa_audit_tenant_sequence", "tenant_id", "sequence_no", unique=True),
        Index("uq_ssa_audit_tenant_hash", "tenant_id", "event_hash", unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(32), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    outcome: Mapped[str] = mapped_column(String(32), nullable=False)
    correlation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False, default="")
    combined_classification: Mapped[str] = mapped_column(String(32), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    timestamp_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=UTC)
    )
    sequence_no: Mapped[int] = mapped_column(BigInteger, nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_hash: Mapped[str] = mapped_column(String(64), nullable=False)
