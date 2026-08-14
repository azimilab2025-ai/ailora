from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from ailora.db.base import Base


class SpaceDataObservationRecord(Base):
    __tablename__ = "space_data_observations"
    __table_args__ = (
        UniqueConstraint("tenant_id", "canonical_digest", name="uq_space_data_tenant_digest"),
        CheckConstraint("advisory_only = true", name="ck_space_data_advisory_only"),
        CheckConstraint("schema_version = '1.0'", name="ck_space_data_schema_version"),
        CheckConstraint("quality = 'VALID'", name="ck_space_data_quality"),
        CheckConstraint("length(canonical_digest) = 64", name="ck_space_data_digest_length"),
        Index("ix_space_data_tenant_object_epoch", "tenant_id", "object_id", "epoch"),
        Index("ix_space_data_tenant_quality_source", "tenant_id", "quality", "source_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    observation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    object_id: Mapped[str] = mapped_column(String(128), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(16), nullable=False)
    reference_frame: Mapped[str] = mapped_column(String(16), nullable=False)
    distance_unit: Mapped[str] = mapped_column(String(16), nullable=False)
    velocity_unit: Mapped[str] = mapped_column(String(16), nullable=False)
    time_scale: Mapped[str] = mapped_column(String(16), nullable=False)
    epoch: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    max_age_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    position: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    velocity: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    covariance: Mapped[list[list[float]] | None] = mapped_column(JSON, nullable=True)
    quality: Mapped[str] = mapped_column(String(16), nullable=False)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_version: Mapped[str] = mapped_column(String(128), nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    canonical_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SpaceDataQuarantineRecord(Base):
    __tablename__ = "space_data_quarantine_records"
    __table_args__ = (
        CheckConstraint("advisory_only = true", name="ck_space_quarantine_advisory_only"),
        CheckConstraint("length(canonical_digest) = 64", name="ck_space_quarantine_digest_length"),
        CheckConstraint("length(reason_detail) <= 512", name="ck_space_quarantine_detail_length"),
        Index("ix_space_quarantine_tenant_created", "tenant_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    canonical_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_detail: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SpaceDataEvidenceRecord(Base):
    __tablename__ = "space_data_ingestion_evidence"
    __table_args__ = (
        CheckConstraint("advisory_only = true", name="ck_space_evidence_advisory_only"),
        CheckConstraint("length(canonical_digest) = 64", name="ck_space_evidence_digest_length"),
        Index("ix_space_evidence_tenant_created", "tenant_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=False)
    canonical_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
