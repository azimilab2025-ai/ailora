from __future__ import annotations

import copy
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from ailora.domain.space_data.contracts import (
    DataQuality,
    DistanceUnit,
    ObservationEnvelope,
    Provenance,
    ReferenceFrame,
    SchemaVersion,
    SpaceDataClassification,
    TimeScale,
    VelocityUnit,
    canonical_payload_digest,
)

NOW = datetime(2026, 8, 14, 18, 45, tzinfo=UTC)


def payload() -> dict[str, object]:
    value: dict[str, object] = {
        "tenant_id": str(uuid.uuid4()),
        "observation_id": "OBS-0001",
        "object_id": "SAT-25544",
        "schema_version": "1.0",
        "reference_frame": "GCRF",
        "distance_unit": "km",
        "velocity_unit": "km/s",
        "time_scale": "UTC",
        "epoch": (NOW - timedelta(seconds=30)).isoformat(),
        "evaluated_at": NOW.isoformat(),
        "max_age_seconds": 30.0,
        "position": [7000.0, 10.0, -2.0],
        "velocity": [0.0, 7.5, 0.1],
        "covariance": None,
        "quality": "VALID",
        "advisory_only": True,
        "provenance": {
            "source_id": "provider-a",
            "source_version": "dataset-2026-08-14",
            "ingested_at": NOW.isoformat(),
            "canonical_digest": "0" * 64,
            "classification": "PUBLIC",
        },
    }
    digest = canonical_payload_digest(value)
    provenance = value["provenance"]
    assert isinstance(provenance, dict)
    provenance["canonical_digest"] = digest
    return value


def test_valid_envelope_is_immutable_and_explicit() -> None:
    envelope = ObservationEnvelope.model_validate(payload())
    assert envelope.schema_version is SchemaVersion.V1
    assert envelope.reference_frame is ReferenceFrame.GCRF
    assert envelope.distance_unit is DistanceUnit.KILOMETER
    assert envelope.velocity_unit is VelocityUnit.KILOMETER_PER_SECOND
    assert envelope.time_scale is TimeScale.UTC
    assert envelope.quality is DataQuality.VALID
    with pytest.raises(ValidationError):
        envelope.object_id = "CHANGED"  # type: ignore[misc]


@pytest.mark.parametrize("version", ["", "0.9", "1.1", "2.0"])
def test_unsupported_schema_versions_fail_closed(version: str) -> None:
    value = payload()
    value["schema_version"] = version
    with pytest.raises(ValidationError):
        ObservationEnvelope.model_validate(value)


@pytest.mark.parametrize("frame", ["", "TEME", "ITRF", "UNKNOWN"])
def test_nonbaseline_or_unknown_frames_are_not_implicitly_converted(frame: str) -> None:
    value = payload()
    value["reference_frame"] = frame
    with pytest.raises(ValidationError):
        ObservationEnvelope.model_validate(value)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [("distance_unit", "m"), ("velocity_unit", "m/s"), ("time_scale", "TAI")],
)
def test_units_and_time_scale_require_explicit_supported_values(field: str, bad_value: str) -> None:
    value = payload()
    value[field] = bad_value
    with pytest.raises(ValidationError):
        ObservationEnvelope.model_validate(value)


def test_exact_freshness_boundary_is_accepted() -> None:
    assert ObservationEnvelope.model_validate(payload()).is_fresh is True


def test_stale_observation_is_rejected() -> None:
    value = payload()
    value["max_age_seconds"] = 29.999
    with pytest.raises(ValidationError, match="stale"):
        ObservationEnvelope.model_validate(value)


def test_future_epoch_beyond_tolerance_is_rejected() -> None:
    value = payload()
    value["epoch"] = (NOW + timedelta(seconds=6)).isoformat()
    with pytest.raises(ValidationError, match="future"):
        ObservationEnvelope.model_validate(value)


def test_naive_time_is_rejected() -> None:
    value = payload()
    value["epoch"] = "2026-08-14T18:44:30"
    with pytest.raises(ValidationError, match="timezone-aware"):
        ObservationEnvelope.model_validate(value)


@pytest.mark.parametrize("object_id", ["", "   ", "bad id", "x" * 129])
def test_object_identity_is_bounded_and_normalized(object_id: str) -> None:
    value = payload()
    value["object_id"] = object_id
    with pytest.raises(ValidationError):
        ObservationEnvelope.model_validate(value)


def test_object_identity_normalization_is_stable() -> None:
    value = payload()
    value["object_id"] = " sat-25544 "
    digest_input = copy.deepcopy(value)
    digest_input["object_id"] = "SAT-25544"
    provenance = value["provenance"]
    assert isinstance(provenance, dict)
    provenance["canonical_digest"] = canonical_payload_digest(digest_input)
    assert ObservationEnvelope.model_validate(value).object_id == "SAT-25544"


def test_nonfinite_vectors_are_rejected() -> None:
    value = payload()
    value["position"] = [7000.0, float("nan"), 0.0]
    with pytest.raises(ValidationError, match="finite"):
        ObservationEnvelope.model_validate(value)


def test_covariance_must_be_finite_six_by_six() -> None:
    value = payload()
    value["covariance"] = [[0.0] * 6 for _ in range(5)]
    with pytest.raises(ValidationError, match="6x6"):
        ObservationEnvelope.model_validate(value)


def test_digest_is_deterministic_and_ignores_supplied_digest() -> None:
    first = payload()
    second = copy.deepcopy(first)
    provenance = second["provenance"]
    assert isinstance(provenance, dict)
    provenance["canonical_digest"] = "f" * 64
    assert canonical_payload_digest(first) == canonical_payload_digest(second)


def test_digest_mismatch_is_rejected() -> None:
    value = payload()
    provenance = value["provenance"]
    assert isinstance(provenance, dict)
    provenance["canonical_digest"] = "f" * 64
    with pytest.raises(ValidationError, match="digest"):
        ObservationEnvelope.model_validate(value)


def test_provenance_and_classification_are_explicit() -> None:
    envelope = ObservationEnvelope.model_validate(payload())
    assert isinstance(envelope.provenance, Provenance)
    assert envelope.provenance.classification is SpaceDataClassification.PUBLIC


def test_operational_clearance_cannot_be_injected() -> None:
    value = payload()
    value["operational_clearance"] = True
    with pytest.raises(ValidationError):
        ObservationEnvelope.model_validate(value)
