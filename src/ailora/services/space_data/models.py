from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from ailora.db.base import Base


class ProviderQualificationRecord(Base):
    __tablename__ = "space_data_provider_qualifications"
    __table_args__ = (
        CheckConstraint("length(terms_digest) = 64", name="ck_provider_terms_digest"),
        CheckConstraint(
            "state IN ('UNQUALIFIED','QUALIFIED','SUSPENDED','REVOKED')",
            name="ck_provider_qualification_state",
        ),
        UniqueConstraint(
            "provider_id",
            "provider_version",
            "terms_digest",
            name="uq_provider_terms",
        ),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_version: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(16), nullable=False)
    license_name: Mapped[str] = mapped_column(String(128), nullable=False)
    terms_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    terms_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewer_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    redistribution_permitted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attribution_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProviderRawArtifactRecord(Base):
    __tablename__ = "space_data_provider_raw_artifacts"
    __table_args__ = (
        CheckConstraint("byte_length > 0", name="ck_provider_raw_positive_length"),
        CheckConstraint("length(payload_digest) = 64", name="ck_provider_raw_digest"),
        CheckConstraint("advisory_only = true", name="ck_provider_raw_advisory"),
        UniqueConstraint(
            "tenant_id", "provider_id", "payload_digest", name="uq_provider_raw_tenant_digest"
        ),
        Index("ix_provider_raw_tenant_object", "tenant_id", "external_object_id", "fetched_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    qualification_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("space_data_provider_qualifications.id", ondelete="RESTRICT"),
        nullable=False,
    )
    request_id: Mapped[str] = mapped_column(String(32), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_version: Mapped[str] = mapped_column(String(64), nullable=False)
    external_object_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    byte_length: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False)
    attribution_text: Mapped[str] = mapped_column(Text, nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProviderAttemptRecord(Base):
    __tablename__ = "space_data_provider_attempts"
    __table_args__ = (
        CheckConstraint("attempt_count > 0", name="ck_provider_attempt_positive"),
        CheckConstraint("advisory_only = true", name="ck_provider_attempt_advisory"),
        Index("ix_provider_attempt_tenant_request", "tenant_id", "request_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    raw_artifact_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("space_data_provider_raw_artifacts.id", ondelete="RESTRICT")
    )
    request_id: Mapped[str] = mapped_column(String(32), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_code: Mapped[str] = mapped_column(String(32), nullable=False)
    error_detail: Mapped[str] = mapped_column(String(256), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False)
