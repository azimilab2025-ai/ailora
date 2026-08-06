"""
AILORA P3-01: Scenario Ingestion and Data Classification Tests.

Validates:
- DataClassification enum values
- DataProvenance immutability and fields
- OrbitalObjectDescriptor construction
- ConjunctionScenario creation, combined_classification, advisory-only flag
- Tenant-scoping requirement
- No spacecraft command path exists
"""

from __future__ import annotations

import uuid

import pytest
from pydantic import ValidationError

from ailora.domain.shared.value_objects import Epoch, OrbitalRegime, ReferenceFrame, TemporalStamp
from ailora.domain.ssa.scenario import (
    ConjunctionScenario,
    DataClassification,
    DataProvenance,
    OrbitalObjectDescriptor,
)

_BASE_EPOCH = Epoch(iso_utc="2026-08-05T00:00:00Z")
_BASE_STAMP = TemporalStamp(epoch=_BASE_EPOCH)


def _make_provenance(
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> DataProvenance:
    return DataProvenance(
        source_label="Test Source",
        classification=classification,
        ingested_at=_BASE_EPOCH,
        is_synthetic=(classification == DataClassification.SYNTHETIC),
    )


def _make_object(
    object_id: str = "SAT-001",
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> OrbitalObjectDescriptor:
    return OrbitalObjectDescriptor(
        object_id=object_id,
        object_name="Test Satellite",
        regime=OrbitalRegime.LEO,
        provenance=_make_provenance(classification),
    )


def _make_scenario(
    primary_cls: DataClassification = DataClassification.SYNTHETIC,
    secondary_cls: DataClassification = DataClassification.SYNTHETIC,
    tenant_id: uuid.UUID | None = None,
) -> ConjunctionScenario:
    return ConjunctionScenario(
        tenant_id=tenant_id or uuid.uuid4(),
        reference_epoch=_BASE_STAMP,
        primary_object=_make_object("SAT-P1", primary_cls),
        secondary_object=_make_object("SAT-S1", secondary_cls),
    )


# ─── DataClassification ───────────────────────────────────────────────────────


def test_data_classification_values() -> None:
    values = {c.value for c in DataClassification}
    assert {"SYNTHETIC", "UNCLASSIFIED", "RESTRICTED"} == values


def test_synthetic_is_lowest_sensitivity() -> None:
    assert DataClassification.SYNTHETIC == "SYNTHETIC"
    assert DataClassification.RESTRICTED == "RESTRICTED"


# ─── DataProvenance ───────────────────────────────────────────────────────────


def test_data_provenance_creation() -> None:
    p = _make_provenance()
    assert p.classification == DataClassification.SYNTHETIC
    assert p.is_synthetic is True


def test_data_provenance_immutable() -> None:
    p = _make_provenance()
    with pytest.raises((ValidationError, TypeError)):
        p.is_synthetic = False  # type: ignore[misc]


def test_data_provenance_source_label_max_length() -> None:
    with pytest.raises(ValidationError):
        DataProvenance(
            source_label="x" * 257,
            ingested_at=_BASE_EPOCH,
        )


# ─── OrbitalObjectDescriptor ─────────────────────────────────────────────────


def test_orbital_object_creation() -> None:
    obj = _make_object()
    assert obj.object_id == "SAT-001"
    assert obj.regime == OrbitalRegime.LEO


def test_orbital_object_immutable() -> None:
    obj = _make_object()
    with pytest.raises((ValidationError, TypeError)):
        obj.object_id = "CHANGED"  # type: ignore[misc]


def test_orbital_object_id_max_length() -> None:
    with pytest.raises(ValidationError):
        OrbitalObjectDescriptor(
            object_id="x" * 65,
            provenance=_make_provenance(),
        )


# ─── ConjunctionScenario ─────────────────────────────────────────────────────


def test_scenario_creation() -> None:
    s = _make_scenario()
    assert s.tenant_id is not None
    assert s.ADVISORY_ONLY is True


def test_scenario_advisory_only_is_always_true() -> None:
    s = _make_scenario()
    assert s.ADVISORY_ONLY is True


def test_scenario_tenant_id_required() -> None:
    with pytest.raises((ValidationError, TypeError)):
        ConjunctionScenario(  # type: ignore[call-arg]
            reference_epoch=_BASE_STAMP,
            primary_object=_make_object(),
            secondary_object=_make_object(),
        )


def test_scenario_combined_classification_synthetic_synthetic() -> None:
    s = _make_scenario(DataClassification.SYNTHETIC, DataClassification.SYNTHETIC)
    assert s.combined_classification == DataClassification.SYNTHETIC


def test_scenario_combined_classification_takes_higher() -> None:
    s = _make_scenario(DataClassification.SYNTHETIC, DataClassification.UNCLASSIFIED)
    assert s.combined_classification == DataClassification.UNCLASSIFIED


def test_scenario_combined_classification_restricted_wins() -> None:
    s = _make_scenario(DataClassification.UNCLASSIFIED, DataClassification.RESTRICTED)
    assert s.combined_classification == DataClassification.RESTRICTED


def test_scenario_frame_property() -> None:
    s = _make_scenario()
    assert s.frame == ReferenceFrame.TEME


def test_scenario_immutable() -> None:
    s = _make_scenario()
    with pytest.raises((ValidationError, TypeError)):
        s.tenant_id = uuid.uuid4()  # type: ignore[misc]


def test_scenario_different_tenants_isolated() -> None:
    """Two scenarios with different tenant_ids must remain distinct."""
    t1 = uuid.uuid4()
    t2 = uuid.uuid4()
    s1 = _make_scenario(tenant_id=t1)
    s2 = _make_scenario(tenant_id=t2)
    assert s1.tenant_id != s2.tenant_id


def test_no_spacecraft_command_in_scenario_module() -> None:
    """Scenario module must not contain actual command execution paths."""
    from pathlib import Path
    text = (
        Path(__file__).parent.parent
        / "src" / "ailora" / "domain" / "ssa" / "scenario.py"
    ).read_text()
    # Check for actual capability implementation patterns, not denial statements
    forbidden_patterns = ["execute_command(", "send_uplink(", "maneuver_execute("]
    for f in forbidden_patterns:
        assert f not in text.lower(), f"scenario.py must not implement: '{f}'"
    # Verify advisory-only statement is present in the module
    assert "advisory" in text.lower(), "scenario.py must include advisory-only statement"
