"""
AILORA P3-06: Audit Trail and Evidence Persistence Tests.

Validates:
- AuditEntry is immutable (frozen dataclass).
- Timestamps must be timezone-aware UTC.
- Detail field must not contain secret patterns.
- AuditLog is append-only.
- entries_for_tenant returns only matching tenant entries.
- entries_for_resource returns only matching resource entries.
- Cross-tenant isolation in audit retrieval.
- No secret leakage in audit fields.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from ailora.domain.ssa.audit import (
    AuditEntry,
    AuditEventType,
    AuditLog,
)

_TENANT = uuid.uuid4()
_ACTOR = uuid.uuid4()
_NOW = datetime.now(tz=UTC)


def _entry(
    tenant_id: uuid.UUID | None = None,
    resource_id: str = "res-001",
    event_type: AuditEventType = AuditEventType.SCENARIO_INGESTED,
    detail: str = "",
) -> AuditEntry:
    return AuditEntry.create(
        tenant_id=tenant_id or _TENANT,
        actor_id=_ACTOR,
        event_type=event_type,
        resource_id=resource_id,
        outcome="SUCCESS",
        detail=detail,
    )


# ─── AuditEntry ───────────────────────────────────────────────────────────────


def test_audit_entry_creation() -> None:
    e = _entry()
    assert e.event_type == AuditEventType.SCENARIO_INGESTED
    assert e.outcome == "SUCCESS"


def test_audit_entry_is_frozen() -> None:
    e = _entry()
    with pytest.raises((TypeError, AttributeError)):
        e.outcome = "CHANGED"  # type: ignore[misc]


def test_audit_entry_timestamp_is_utc_aware() -> None:
    e = _entry()
    assert e.timestamp_utc.tzinfo is not None


def test_audit_entry_naive_timestamp_raises() -> None:
    with pytest.raises(ValueError):
        AuditEntry(
            entry_id=uuid.uuid4(),
            tenant_id=_TENANT,
            actor_id=_ACTOR,
            event_type=AuditEventType.SCENARIO_INGESTED,
            resource_id="r1",
            outcome="OK",
            timestamp_utc=datetime(2026, 8, 5, 0, 0, 0),  # naive — no tzinfo
        )


def test_audit_entry_secret_in_detail_raises() -> None:
    with pytest.raises(ValueError):
        _entry(detail="password=mysecret123")


def test_audit_entry_detail_safe_text_ok() -> None:
    e = _entry(detail="Scenario ingested successfully at T0")
    assert "successfully" in e.detail


def test_audit_entry_correlation_id_stored() -> None:
    e = AuditEntry.create(
        tenant_id=_TENANT,
        actor_id=_ACTOR,
        event_type=AuditEventType.SCENARIO_SCREENED,
        resource_id="s-001",
        outcome="SUCCESS",
        correlation_id="corr-abc-123",
    )
    assert e.correlation_id == "corr-abc-123"


def test_audit_entry_event_types_enumerated() -> None:
    types = {e.value for e in AuditEventType}
    required = {
        "SCENARIO_INGESTED", "SCENARIO_SCREENED", "SCENARIO_RISK_ASSESSED",
        "REVIEW_OPENED", "REVIEW_STATE_CHANGED", "REVIEW_CLOSED",
        "ACCESS_GRANTED", "ACCESS_DENIED",
    }
    assert required.issubset(types)


# ─── AuditLog ─────────────────────────────────────────────────────────────────


def test_audit_log_starts_empty() -> None:
    log = AuditLog()
    assert log.total_entries == 0


def test_audit_log_append_increments_count() -> None:
    log = AuditLog()
    log.append(_entry())
    assert log.total_entries == 1
    log.append(_entry())
    assert log.total_entries == 2


def test_audit_log_entries_for_tenant() -> None:
    log = AuditLog()
    t1 = uuid.uuid4()
    t2 = uuid.uuid4()
    log.append(_entry(tenant_id=t1))
    log.append(_entry(tenant_id=t1))
    log.append(_entry(tenant_id=t2))
    assert len(log.entries_for_tenant(t1)) == 2
    assert len(log.entries_for_tenant(t2)) == 1


def test_audit_log_cross_tenant_isolation() -> None:
    """entries_for_tenant must not return other tenants' records."""
    log = AuditLog()
    t1 = uuid.uuid4()
    t2 = uuid.uuid4()
    log.append(_entry(tenant_id=t1))
    log.append(_entry(tenant_id=t2))
    for entry in log.entries_for_tenant(t1):
        assert entry.tenant_id == t1
        assert entry.tenant_id != t2


def test_audit_log_entries_for_resource() -> None:
    log = AuditLog()
    log.append(_entry(resource_id="scenario-001"))
    log.append(_entry(resource_id="scenario-001"))
    log.append(_entry(resource_id="scenario-002"))
    assert len(log.entries_for_resource("scenario-001")) == 2
    assert len(log.entries_for_resource("scenario-002")) == 1


def test_audit_log_empty_tenant_returns_empty() -> None:
    log = AuditLog()
    log.append(_entry())
    assert log.entries_for_tenant(uuid.uuid4()) == []
