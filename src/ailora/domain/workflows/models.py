"""Pure durable-workflow state and retry contracts."""

from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from ailora.db.base import Base

_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{7,127}$")


class WorkflowState(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    RETRY_WAIT = "RETRY_WAIT"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class FailureKind(StrEnum):
    RETRYABLE = "RETRYABLE"
    PERMANENT = "PERMANENT"
    TIMEOUT = "TIMEOUT"
    STALE_WORKER = "STALE_WORKER"


class WorkflowContractError(ValueError):
    """A workflow input or transition violates the bounded contract."""


_ALLOWED: dict[WorkflowState, frozenset[WorkflowState]] = {
    WorkflowState.PENDING: frozenset({WorkflowState.RUNNING, WorkflowState.CANCELLED}),
    WorkflowState.RUNNING: frozenset(
        {
            WorkflowState.SUCCEEDED,
            WorkflowState.RETRY_WAIT,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }
    ),
    WorkflowState.RETRY_WAIT: frozenset(
        {WorkflowState.RUNNING, WorkflowState.FAILED, WorkflowState.CANCELLED}
    ),
    WorkflowState.SUCCEEDED: frozenset(),
    WorkflowState.FAILED: frozenset(),
    WorkflowState.CANCELLED: frozenset(),
}


def validate_transition(current: WorkflowState, target: WorkflowState) -> None:
    if target not in _ALLOWED[current]:
        raise WorkflowContractError(
            f"invalid workflow transition: {current.value} -> {target.value}"
        )


def validate_idempotency_key(value: str) -> str:
    normalized = value.strip()
    if not _KEY.fullmatch(normalized):
        raise WorkflowContractError("idempotency key must be 8-128 bounded safe characters")
    return normalized


def deterministic_backoff_seconds(
    attempt: int, *, base_seconds: float = 1.0, cap_seconds: float = 60.0
) -> float:
    if attempt < 1 or not math.isfinite(base_seconds) or not math.isfinite(cap_seconds):
        raise WorkflowContractError("retry configuration is invalid")
    if base_seconds <= 0.0 or cap_seconds < base_seconds:
        raise WorkflowContractError("retry configuration is invalid")
    return float(min(cap_seconds, base_seconds * (2 ** (attempt - 1))))


@dataclass(frozen=True, slots=True)
class WorkflowRequest:
    tenant_id: uuid.UUID
    actor_user_id: uuid.UUID
    idempotency_key: str
    workflow_type: str
    payload_digest: str
    correlation_id: uuid.UUID
    causation_id: uuid.UUID | None = None
    max_attempts: int = 3
    advisory_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "idempotency_key", validate_idempotency_key(self.idempotency_key))
        if not self.workflow_type.strip() or len(self.workflow_type) > 64:
            raise WorkflowContractError("workflow type is required and bounded")
        if not re.fullmatch(r"[0-9a-f]{64}", self.payload_digest):
            raise WorkflowContractError("payload digest must be lowercase sha256")
        if not 1 <= self.max_attempts <= 10:
            raise WorkflowContractError("max attempts must be between 1 and 10")
        if self.advisory_only is not True:
            raise WorkflowContractError("workflow must remain advisory-only")

    @property
    def request_digest(self) -> str:
        payload = {
            "actor_user_id": str(self.actor_user_id),
            "causation_id": str(self.causation_id) if self.causation_id else None,
            "correlation_id": str(self.correlation_id),
            "idempotency_key": self.idempotency_key,
            "max_attempts": self.max_attempts,
            "payload_digest": self.payload_digest,
            "tenant_id": str(self.tenant_id),
            "workflow_type": self.workflow_type,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class WorkflowEvent:
    sequence_number: int
    event_type: str
    from_state: WorkflowState | None
    to_state: WorkflowState
    correlation_id: uuid.UUID
    causation_id: uuid.UUID | None
    actor_user_id: uuid.UUID
    occurred_at: datetime
    evidence_digest: str

    def __post_init__(self) -> None:
        if self.sequence_number < 1 or self.occurred_at.tzinfo is None:
            raise WorkflowContractError("event sequence and timestamp must be valid")
        if not re.fullmatch(r"[0-9a-f]{64}", self.evidence_digest):
            raise WorkflowContractError("event evidence digest is invalid")
        object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(UTC))


class WorkflowRecord(Base):
    __tablename__ = "durable_workflows"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_workflow_tenant_idempotency"),
        CheckConstraint(
            "attempt_count >= 0 AND attempt_count <= max_attempts",
            name="ck_workflow_attempt_bounds",
        ),
        CheckConstraint(
            "max_attempts >= 1 AND max_attempts <= 10", name="ck_workflow_max_attempts"
        ),
        CheckConstraint("advisory_only", name="ck_workflow_advisory_only"),
        Index("ix_workflow_tenant_state_next", "tenant_id", "state", "next_attempt_at"),
    )
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    workflow_type: Mapped[str] = mapped_column(String(64), nullable=False)
    request_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    correlation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    causation_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True))
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    event_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_kind: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    error_code: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    lease_token: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True))
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=UTC)
    )


class WorkflowEventRecord(Base):
    __tablename__ = "durable_workflow_events"
    __table_args__ = (
        UniqueConstraint("workflow_id", "sequence_number", name="uq_workflow_event_sequence"),
        CheckConstraint("sequence_number > 0", name="ck_workflow_event_sequence"),
        CheckConstraint("advisory_only", name="ck_workflow_event_advisory"),
        Index("ix_workflow_event_tenant_correlation", "tenant_id", "correlation_id"),
    )
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("durable_workflows.id", ondelete="CASCADE"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    from_state: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    to_state: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    correlation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    causation_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True))
    evidence_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=UTC)
    )
