from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from ailora.recovery.qualification import (
    ISOLATED_ENVIRONMENT,
    LOCAL_STATUS,
    REQUIRED_RECOVERY_CHECKS,
    RecoveryQualificationError,
    RecoveryTimeline,
    RecoveryValidation,
    create_recovery_observation,
    verify_recovery_observation,
)


def _timeline() -> RecoveryTimeline:
    start = datetime(2026, 8, 17, 8, 0, tzinfo=UTC)
    return RecoveryTimeline(
        recovery_point_utc=start,
        incident_declared_utc=start + timedelta(seconds=30),
        writes_fenced_utc=start + timedelta(seconds=40),
        restore_started_utc=start + timedelta(seconds=50),
        integrity_validated_utc=start + timedelta(seconds=80),
        serving_validated_utc=start + timedelta(seconds=100),
        reconciliation_completed_utc=start + timedelta(seconds=120),
    )


def _validation() -> RecoveryValidation:
    return RecoveryValidation(
        drill_id="local-drill-001",
        topology_id="sqlite-isolated-fixture",
        environment=ISOLATED_ENVIRONMENT,
        passed_checks=REQUIRED_RECOVERY_CHECKS,
        evidence_refs=("evidence/local-drill-001.json",),
        isolated_restore=True,
    )


def test_observed_rpo_rto_rco_use_validated_serving_and_reconciliation() -> None:
    timeline = _timeline()
    assert timeline.observed_rpo_seconds == 30
    assert timeline.observed_rto_seconds == 70
    assert timeline.observed_rco_seconds == 90


def test_observation_is_deterministic_digest_bound_and_explicitly_local() -> None:
    document = create_recovery_observation(_timeline(), _validation())
    assert document == create_recovery_observation(_timeline(), _validation())
    payload = verify_recovery_observation(document)
    assert payload["status"] == LOCAL_STATUS
    assert payload["production_authorized"] is False
    assert payload["objectives"] == {"rpo": None, "rto": None, "rco": None}


@pytest.mark.parametrize(
    "field",
    [
        "incident_declared_utc",
        "writes_fenced_utc",
        "restore_started_utc",
        "integrity_validated_utc",
        "serving_validated_utc",
        "reconciliation_completed_utc",
    ],
)
def test_naive_timeline_timestamp_is_rejected(field: str) -> None:
    values = vars(_timeline()) | {field: datetime(2026, 8, 17, 8, 0)}
    with pytest.raises(RecoveryQualificationError, match="timezone-aware"):
        RecoveryTimeline(**values)


@pytest.mark.parametrize(
    "field",
    [
        "incident_declared_utc",
        "writes_fenced_utc",
        "restore_started_utc",
        "integrity_validated_utc",
        "serving_validated_utc",
    ],
)
def test_non_monotonic_recovery_stage_is_rejected(field: str) -> None:
    timeline = _timeline()
    values = vars(timeline) | {field: timeline.reconciliation_completed_utc + timedelta(seconds=1)}
    with pytest.raises(RecoveryQualificationError, match="monotonic"):
        RecoveryTimeline(**values)


def test_missing_required_check_is_rejected() -> None:
    with pytest.raises(RecoveryQualificationError, match="checks missing"):
        replace(
            _validation(),
            passed_checks=REQUIRED_RECOVERY_CHECKS - {"deletion_suppression"},
        )


def test_unknown_check_is_rejected() -> None:
    with pytest.raises(RecoveryQualificationError, match="unknown recovery"):
        replace(_validation(), passed_checks=REQUIRED_RECOVERY_CHECKS | {"marketing_claim"})


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"environment": "production"}, "isolated local"),
        ({"isolated_restore": False}, "isolated local"),
        ({"production_authorized": True}, "cannot authorize production"),
        ({"evidence_refs": ()}, "evidence references"),
        ({"evidence_refs": ("https://provider.example/backup",)}, "evidence references"),
    ],
)
def test_unsafe_validation_scope_is_rejected(changes: dict[str, object], message: str) -> None:
    with pytest.raises(RecoveryQualificationError, match=message):
        replace(_validation(), **changes)


def test_payload_tampering_is_rejected() -> None:
    envelope = json.loads(create_recovery_observation(_timeline(), _validation()))
    envelope["payload"]["observed_seconds"]["rto"] = 1
    with pytest.raises(RecoveryQualificationError, match="digest mismatch"):
        verify_recovery_observation(json.dumps(envelope))


def test_boundary_tampering_is_rejected_even_with_recomputed_digest() -> None:
    envelope = json.loads(create_recovery_observation(_timeline(), _validation()))
    envelope["payload"]["status"] = "PRODUCTION_QUALIFIED"
    import hashlib

    payload = json.dumps(envelope["payload"], sort_keys=True, separators=(",", ":")).encode()
    envelope["sha256"] = hashlib.sha256(payload).hexdigest()
    with pytest.raises(RecoveryQualificationError, match="boundary is invalid"):
        verify_recovery_observation(json.dumps(envelope))


@pytest.mark.parametrize("document", ["not-json", "[]", '{"payload":{}}'])
def test_malformed_observation_is_rejected(document: str) -> None:
    with pytest.raises(RecoveryQualificationError):
        verify_recovery_observation(document)
