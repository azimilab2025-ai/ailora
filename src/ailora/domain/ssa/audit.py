"""
AILORA Audit Trail and Evidence Persistence.

Implements an immutable append-only audit log for all conjunction risk
assessment lifecycle events.

Security requirements (Prompt 15 §23):
- Tenant, Actor, Action, Resource, Outcome, Timestamp are always recorded.
- Secrets, tokens, passwords, raw authorization headers, and PII
  must NEVER appear in audit records.
- Audit entries are immutable once written (append-only).
- Timestamps are UTC.
- Correlation IDs must be carried across boundaries.

No spacecraft command path — permanently denied.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

# ---------------------------------------------------------------------------
# Audit event types
# ---------------------------------------------------------------------------


class AuditEventType(StrEnum):
    """Categories of auditable events in the AILORA system."""

    # Scenario lifecycle
    SCENARIO_INGESTED = "SCENARIO_INGESTED"
    SCENARIO_SCREENED = "SCENARIO_SCREENED"
    SCENARIO_RISK_ASSESSED = "SCENARIO_RISK_ASSESSED"

    # Review lifecycle
    REVIEW_OPENED = "REVIEW_OPENED"
    REVIEW_STATE_CHANGED = "REVIEW_STATE_CHANGED"
    REVIEW_CLOSED = "REVIEW_CLOSED"

    # Authentication (no credential values)
    USER_AUTHENTICATED = "USER_AUTHENTICATED"
    USER_AUTH_FAILED = "USER_AUTH_FAILED"

    # Authorization
    ACCESS_GRANTED = "ACCESS_GRANTED"
    ACCESS_DENIED = "ACCESS_DENIED"


# ---------------------------------------------------------------------------
# Audit entry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AuditEntry:
    """
    An immutable audit record.

    Attributes:
        entry_id:       Unique identifier for this audit entry.
        tenant_id:      Owning tenant (required for all tenant-scoped events).
        actor_id:       User or service performing the action.
        event_type:     Categorized event type.
        resource_id:    Identifier of the affected resource (scenario, review, etc.).
        outcome:        Machine-readable outcome string (e.g. "SUCCESS", "DENIED").
        timestamp_utc:  UTC timestamp of the event.
        correlation_id: Optional correlation ID for tracing.
        detail:         Optional human-readable context (must not contain secrets).

    Security invariants:
        - No secret, token, password, or PII is stored in any field.
        - `detail` is human-readable advisory text only.
        - Entry is frozen (immutable) once created.
    """

    entry_id: uuid.UUID
    tenant_id: uuid.UUID
    actor_id: uuid.UUID
    event_type: AuditEventType
    resource_id: str
    outcome: str
    timestamp_utc: datetime
    correlation_id: str = ""
    detail: str = ""

    def __post_init__(self) -> None:
        """Enforce security invariants on construction."""
        if self.timestamp_utc.tzinfo is None:
            raise ValueError("AuditEntry.timestamp_utc must be timezone-aware (UTC)")
        # Enforce that detail does not contain obvious secret patterns
        _check_no_secret(self.detail, field_name="detail")

    @classmethod
    def create(
        cls,
        tenant_id: uuid.UUID,
        actor_id: uuid.UUID,
        event_type: AuditEventType,
        resource_id: str,
        outcome: str,
        correlation_id: str = "",
        detail: str = "",
    ) -> AuditEntry:
        """Factory method with auto-generated entry_id and current UTC timestamp."""
        return cls(
            entry_id=uuid.uuid4(),
            tenant_id=tenant_id,
            actor_id=actor_id,
            event_type=event_type,
            resource_id=resource_id,
            outcome=outcome,
            timestamp_utc=datetime.now(tz=UTC),
            correlation_id=correlation_id,
            detail=detail,
        )


def _check_no_secret(text: str, field_name: str) -> None:
    """Raise ValueError if text contains patterns that look like secrets."""
    # Detect obvious secret injection patterns
    forbidden = ["password=", "secret=", "token=Bearer", "api_key="]
    lower = text.lower()
    for pattern in forbidden:
        if pattern in lower:
            raise ValueError(
                f"AuditEntry.{field_name} must not contain secret pattern: '{pattern}'"
            )


# ---------------------------------------------------------------------------
# In-memory audit log (PHASE_3 baseline — will be persisted in PHASE_4)
# ---------------------------------------------------------------------------


@dataclass
class AuditLog:
    """
    An in-memory append-only audit log.

    PHASE_3 implementation: entries are held in memory only.
    Persistence to the database will be added when PHASE_4 (workflow/events)
    is implemented.

    Invariant: entries may only be appended, never modified or deleted.
    """

    _entries: list[AuditEntry] = field(default_factory=list)

    def append(self, entry: AuditEntry) -> None:
        """Append an audit entry. Entries are immutable once appended."""
        self._entries.append(entry)

    def entries_for_tenant(self, tenant_id: uuid.UUID) -> list[AuditEntry]:
        """Return all entries belonging to a specific tenant."""
        return [e for e in self._entries if e.tenant_id == tenant_id]

    def entries_for_resource(self, resource_id: str) -> list[AuditEntry]:
        """Return all entries for a specific resource (e.g. scenario_id)."""
        return [e for e in self._entries if e.resource_id == resource_id]

    @property
    def total_entries(self) -> int:
        return len(self._entries)
