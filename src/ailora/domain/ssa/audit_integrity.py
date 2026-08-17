"""Canonical SHA-256 chain construction and verification for audit evidence."""

from __future__ import annotations

import hashlib
import re
import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Protocol

GENESIS_HASH = "0" * 64
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class AuditChainRecord(Protocol):
    """Fields required to reconstruct and verify one persisted audit event."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    actor_user_id: uuid.UUID
    event_type: str
    resource_type: str
    resource_id: uuid.UUID
    outcome: str
    correlation_id: uuid.UUID
    detail: str
    combined_classification: str
    advisory_only: bool
    timestamp_utc: datetime
    sequence_no: int
    previous_hash: str
    event_hash: str


class AuditIntegrityError(ValueError):
    """The audit chain is malformed, discontinuous, or cryptographically invalid."""


def _component(value: str) -> str:
    encoded = value.encode("utf-8")
    return f"{len(encoded)}:{value}"


def _utc_timestamp(value: datetime) -> str:
    normalized = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    return normalized.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def canonical_audit_payload(record: AuditChainRecord) -> str:
    """Return the length-prefixed canonical payload shared with PostgreSQL."""
    values = (
        str(record.tenant_id),
        str(record.id),
        str(record.actor_user_id),
        record.event_type,
        record.resource_type,
        str(record.resource_id),
        record.outcome,
        str(record.correlation_id),
        record.detail,
        record.combined_classification,
        "true" if record.advisory_only else "false",
        _utc_timestamp(record.timestamp_utc),
    )
    return "".join(_component(value) for value in values)


def compute_event_hash(*, previous_hash: str, payload: str) -> str:
    """Bind one canonical event to its predecessor with SHA-256."""
    if not _SHA256_PATTERN.fullmatch(previous_hash):
        raise AuditIntegrityError("previous audit hash must be lowercase SHA-256")
    return hashlib.sha256(f"{previous_hash}{payload}".encode()).hexdigest()


def assign_chain_values(
    record: AuditChainRecord,
    *,
    previous_sequence: int | None,
    previous_hash: str | None,
) -> None:
    """Assign deterministic next-link values before persistence."""
    predecessor = previous_hash or GENESIS_HASH
    record.sequence_no = 1 if previous_sequence is None else previous_sequence + 1
    record.previous_hash = predecessor
    record.event_hash = compute_event_hash(
        previous_hash=predecessor,
        payload=canonical_audit_payload(record),
    )


def verify_audit_chain(records: Sequence[AuditChainRecord]) -> None:
    """Fail closed unless every event forms one ordered tenant-specific chain."""
    if not records:
        return
    tenant_id = records[0].tenant_id
    expected_previous_hash = GENESIS_HASH
    for expected_sequence, record in enumerate(records, start=1):
        if record.tenant_id != tenant_id:
            raise AuditIntegrityError("audit chain crosses tenant boundary")
        if record.sequence_no != expected_sequence:
            raise AuditIntegrityError("audit sequence is discontinuous")
        if record.previous_hash != expected_previous_hash:
            raise AuditIntegrityError("audit predecessor hash is discontinuous")
        expected_hash = compute_event_hash(
            previous_hash=expected_previous_hash,
            payload=canonical_audit_payload(record),
        )
        if record.event_hash != expected_hash:
            raise AuditIntegrityError("audit event hash mismatch")
        expected_previous_hash = record.event_hash
