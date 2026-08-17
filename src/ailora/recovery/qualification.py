"""Bounded recovery evidence for isolated drills, never production qualification."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final

OBSERVATION_SCHEMA: Final = "AILORA-RECOVERY-OBSERVATION-V1"
LOCAL_STATUS: Final = "LOCAL_OBSERVATION_NOT_PRODUCTION_RPO_RTO_QUALIFICATION"
ISOLATED_ENVIRONMENT: Final = "isolated-local-recovery-drill"
REQUIRED_RECOVERY_CHECKS: Final = frozenset(
    {
        "audit_integrity",
        "authorization_and_revocation",
        "deletion_suppression",
        "schema_head",
        "sqlite_integrity",
        "tenant_isolation",
        "validated_serving",
    }
)


class RecoveryQualificationError(ValueError):
    """Recovery evidence is incomplete, unsafe, malformed, or overstated."""


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise RecoveryQualificationError(f"{field} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


@dataclass(frozen=True)
class RecoveryTimeline:
    """Monotonic incident timeline used for observed RPO, RTO and RCO."""

    recovery_point_utc: datetime
    incident_declared_utc: datetime
    writes_fenced_utc: datetime
    restore_started_utc: datetime
    integrity_validated_utc: datetime
    serving_validated_utc: datetime
    reconciliation_completed_utc: datetime

    def __post_init__(self) -> None:
        fields = (
            "recovery_point_utc",
            "incident_declared_utc",
            "writes_fenced_utc",
            "restore_started_utc",
            "integrity_validated_utc",
            "serving_validated_utc",
            "reconciliation_completed_utc",
        )
        normalized = tuple(_utc(getattr(self, field), field) for field in fields)
        for field, value in zip(fields, normalized, strict=True):
            object.__setattr__(self, field, value)
        if list(normalized) != sorted(normalized):
            raise RecoveryQualificationError("recovery timeline must be monotonic")

    @property
    def observed_rpo_seconds(self) -> float:
        return (self.incident_declared_utc - self.recovery_point_utc).total_seconds()

    @property
    def observed_rto_seconds(self) -> float:
        return (self.serving_validated_utc - self.incident_declared_utc).total_seconds()

    @property
    def observed_rco_seconds(self) -> float:
        return (self.reconciliation_completed_utc - self.incident_declared_utc).total_seconds()


@dataclass(frozen=True)
class RecoveryValidation:
    """Scope and evidence required before recording one local recovery observation."""

    drill_id: str
    topology_id: str
    environment: str
    passed_checks: frozenset[str]
    evidence_refs: tuple[str, ...]
    isolated_restore: bool
    production_authorized: bool = False

    def __post_init__(self) -> None:
        if not self.drill_id.strip() or not self.topology_id.strip():
            raise RecoveryQualificationError("drill and topology identifiers are required")
        if self.environment != ISOLATED_ENVIRONMENT or not self.isolated_restore:
            raise RecoveryQualificationError("only an isolated local restore may be observed")
        if self.production_authorized:
            raise RecoveryQualificationError("this contract cannot authorize production recovery")
        missing = REQUIRED_RECOVERY_CHECKS - self.passed_checks
        if missing:
            raise RecoveryQualificationError(f"required recovery checks missing: {sorted(missing)}")
        if self.passed_checks - REQUIRED_RECOVERY_CHECKS:
            raise RecoveryQualificationError("unknown recovery checks are not accepted")
        if not self.evidence_refs or any(
            not ref.strip() or "://" in ref for ref in self.evidence_refs
        ):
            raise RecoveryQualificationError("local evidence references are required")


def _payload(timeline: RecoveryTimeline, validation: RecoveryValidation) -> dict[str, object]:
    return {
        "schema": OBSERVATION_SCHEMA,
        "status": LOCAL_STATUS,
        "drill_id": validation.drill_id,
        "topology_id": validation.topology_id,
        "environment": validation.environment,
        "isolated_restore": validation.isolated_restore,
        "production_authorized": False,
        "timeline_utc": {
            "recovery_point": _timestamp(timeline.recovery_point_utc),
            "incident_declared": _timestamp(timeline.incident_declared_utc),
            "writes_fenced": _timestamp(timeline.writes_fenced_utc),
            "restore_started": _timestamp(timeline.restore_started_utc),
            "integrity_validated": _timestamp(timeline.integrity_validated_utc),
            "serving_validated": _timestamp(timeline.serving_validated_utc),
            "reconciliation_completed": _timestamp(timeline.reconciliation_completed_utc),
        },
        "observed_seconds": {
            "rpo": timeline.observed_rpo_seconds,
            "rto": timeline.observed_rto_seconds,
            "rco": timeline.observed_rco_seconds,
        },
        "passed_checks": sorted(validation.passed_checks),
        "evidence_refs": list(validation.evidence_refs),
        "objectives": {"rpo": None, "rto": None, "rco": None},
    }


def _canonical(value: Mapping[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def create_recovery_observation(
    timeline: RecoveryTimeline,
    validation: RecoveryValidation,
) -> str:
    """Create a deterministic digest-bound local recovery observation."""
    payload = _payload(timeline, validation)
    envelope = {
        "payload": payload,
        "sha256": hashlib.sha256(_canonical(payload)).hexdigest(),
    }
    return json.dumps(envelope, sort_keys=True, separators=(",", ":"))


def verify_recovery_observation(document: str) -> Mapping[str, object]:
    """Fail closed unless an observation is intact and preserves every boundary."""
    try:
        envelope = json.loads(document)
    except json.JSONDecodeError as exc:
        raise RecoveryQualificationError("recovery observation is not valid JSON") from exc
    if not isinstance(envelope, dict) or set(envelope) != {"payload", "sha256"}:
        raise RecoveryQualificationError("recovery observation envelope is malformed")
    payload = envelope["payload"]
    digest = envelope["sha256"]
    if not isinstance(payload, dict) or not isinstance(digest, str):
        raise RecoveryQualificationError("recovery observation types are malformed")
    if hashlib.sha256(_canonical(payload)).hexdigest() != digest:
        raise RecoveryQualificationError("recovery observation digest mismatch")
    if payload.get("schema") != OBSERVATION_SCHEMA or payload.get("status") != LOCAL_STATUS:
        raise RecoveryQualificationError("recovery observation boundary is invalid")
    if payload.get("environment") != ISOLATED_ENVIRONMENT:
        raise RecoveryQualificationError("recovery observation environment is invalid")
    if (
        payload.get("isolated_restore") is not True
        or payload.get("production_authorized") is not False
    ):
        raise RecoveryQualificationError("recovery observation authority is invalid")
    if set(payload.get("passed_checks", [])) != REQUIRED_RECOVERY_CHECKS:
        raise RecoveryQualificationError("recovery observation checks are incomplete")
    if payload.get("objectives") != {"rpo": None, "rto": None, "rco": None}:
        raise RecoveryQualificationError("unapproved recovery objectives were introduced")
    return payload
