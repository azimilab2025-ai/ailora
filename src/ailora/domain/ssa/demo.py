"""
AILORA Vertical Slice Demo Scenario.

A complete end-to-end reproducible demo of the conjunction risk assessment
pipeline (PHASE_3 vertical slice).

This scenario uses ONLY SYNTHETIC data. No real orbital objects, real
TLE data, or live external services are involved.

Scientific boundary (Prompt 06):
  All outputs are Advisory, Bounded, PHY-C1/T0 tier, Non-normative.
  SENTINEL: DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED.

Demo scenario: SYNTH-SAT-A and SYNTH-SAT-B at a common epoch,
with a configurable separation distance.

Expected outputs are deterministic given fixed inputs.

No spacecraft command path — permanently denied.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from ailora.domain.shared.value_objects import (
    CartesianState,
    Epoch,
    OrbitalRegime,
    ReferenceFrame,
    TemporalStamp,
)
from ailora.domain.ssa.audit import AuditEntry, AuditEventType, AuditLog
from ailora.domain.ssa.review import ReviewRecord, ReviewState
from ailora.domain.ssa.risk import ConjunctionRiskAssessment, assess_conjunction_risk
from ailora.domain.ssa.scenario import (
    ConjunctionScenario,
    DataClassification,
    DataProvenance,
    OrbitalObjectDescriptor,
)
from ailora.domain.ssa.screening import ConjunctionScreeningResult, screen_t0_phy_c1
from ailora.domain.ssa.tle_parser import TLERecord, parse_tle

# ---------------------------------------------------------------------------
# Demo synthetic TLE data
# ---------------------------------------------------------------------------

# Synthetic ISS-like object (based on public NORAD catalog format — SYNTHETIC)
DEMO_TLE_LINE0_A = "SYNTH-SAT-A"
DEMO_TLE_LINE1_A = "1 99001U 26001A   26217.50000000  .00000000  00000-0  00000-0 0  9991"
DEMO_TLE_LINE2_A = "2 99001  51.6000   0.0000 0001000   0.0000   0.0000 15.49000000000001"

DEMO_TLE_LINE0_B = "SYNTH-SAT-B"
DEMO_TLE_LINE1_B = "1 99002U 26001B   26217.50000000  .00000000  00000-0  00000-0 0  9992"
DEMO_TLE_LINE2_B = "2 99002  51.6000   0.0000 0001000   0.0000   0.5000 15.49000000000001"

# Demo epoch
DEMO_EPOCH_ISO = "2026-08-05T12:00:00Z"

# Demo separation distances (metres)
DEMO_SEPARATION_CLOSE_M = 3_000.0  # 3 km — within default CDT
DEMO_SEPARATION_FAR_M = 500_000.0  # 500 km — well outside CDT


# ---------------------------------------------------------------------------
# Demo result container
# ---------------------------------------------------------------------------


@dataclass
class DemoScenarioResult:
    """
    Complete result of running the AILORA vertical slice demo.

    All fields are advisory-only and non-normative.
    """

    # Inputs
    tenant_id: uuid.UUID
    tle_a: TLERecord
    tle_b: TLERecord

    # Pipeline outputs
    scenario: ConjunctionScenario
    screening_result: ConjunctionScreeningResult
    risk_assessment: ConjunctionRiskAssessment
    review_record: ReviewRecord
    audit_log: AuditLog

    # Advisory sentinel
    is_advisory: bool = True
    advisory_label: str = (
        "AILORA DEMO — Advisory Only | PHY-C1/T0 | Non-normative | Prompt 06 DOMAIN_REVIEW_REQUIRED"
    )


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------


def run_demo_scenario(
    separation_m: float = DEMO_SEPARATION_CLOSE_M,
    conjunction_distance_threshold_km: float = 5.0,
) -> DemoScenarioResult:
    """
    Run the complete AILORA vertical slice demo pipeline.

    Advisory-only. Non-normative. PHY-C1/T0 tier.
    See module docstring for Prompt 06 boundary.

    Args:
        separation_m:   Separation between the two synthetic objects in metres.
        conjunction_distance_threshold_km: CDT for PHY-C1 screening (km).

    Returns:
        DemoScenarioResult with all pipeline outputs.
    """
    tenant_id = uuid.uuid4()
    actor_id = uuid.uuid4()
    audit_log = AuditLog()

    # --- Step 1: Parse synthetic TLEs ---
    tle_a = parse_tle(DEMO_TLE_LINE0_A, DEMO_TLE_LINE1_A, DEMO_TLE_LINE2_A)
    tle_b = parse_tle(DEMO_TLE_LINE0_B, DEMO_TLE_LINE1_B, DEMO_TLE_LINE2_B)

    # --- Step 2: Build scenario ---
    epoch = Epoch(iso_utc=DEMO_EPOCH_ISO)
    stamp = TemporalStamp(epoch=epoch, frame=ReferenceFrame.TEME)

    provenance = DataProvenance(
        source_label="AILORA Demo — Synthetic Data",
        classification=DataClassification.SYNTHETIC,
        ingested_at=epoch,
        is_synthetic=True,
    )
    obj_a = OrbitalObjectDescriptor(
        object_id=tle_a.catalog_number,
        object_name=tle_a.name,
        regime=OrbitalRegime.LEO,
        provenance=provenance,
    )
    obj_b = OrbitalObjectDescriptor(
        object_id=tle_b.catalog_number,
        object_name=tle_b.name,
        regime=OrbitalRegime.LEO,
        provenance=provenance,
    )
    scenario = ConjunctionScenario(
        tenant_id=tenant_id,
        reference_epoch=stamp,
        primary_object=obj_a,
        secondary_object=obj_b,
        ingestion_notes="AILORA Phase 3 demo scenario — synthetic data only",
    )

    audit_log.append(
        AuditEntry.create(
            tenant_id=tenant_id,
            actor_id=actor_id,
            event_type=AuditEventType.SCENARIO_INGESTED,
            resource_id=str(scenario.scenario_id),
            outcome="SUCCESS",
            detail="Scenario ingested: synthetic demo",
        )
    )

    # --- Step 3: Build state vectors ---
    # Primary object at some representative LEO position
    primary_state = CartesianState(
        stamp=stamp,
        x_m=7_000_000.0,
        y_m=0.0,
        z_m=0.0,
        vx_ms=0.0,
        vy_ms=7_500.0,
        vz_ms=0.0,
    )
    # Secondary object offset by the demo separation
    secondary_state = CartesianState(
        stamp=stamp,
        x_m=7_000_000.0 + separation_m,
        y_m=0.0,
        z_m=0.0,
        vx_ms=0.0,
        vy_ms=7_500.0,
        vz_ms=0.0,
    )

    # --- Step 4: T0/PHY-C1 screening ---
    screening_result = screen_t0_phy_c1(
        primary_state,
        secondary_state,
        conjunction_distance_threshold_km=conjunction_distance_threshold_km,
    )

    audit_log.append(
        AuditEntry.create(
            tenant_id=tenant_id,
            actor_id=actor_id,
            event_type=AuditEventType.SCENARIO_SCREENED,
            resource_id=str(scenario.scenario_id),
            outcome=screening_result.outcome.value,
            detail=f"PHY-C1 screening: dist={screening_result.distance_km:.3f} km",
        )
    )

    # --- Step 5: Risk assessment ---
    risk_assessment = assess_conjunction_risk(screening_result)

    audit_log.append(
        AuditEntry.create(
            tenant_id=tenant_id,
            actor_id=actor_id,
            event_type=AuditEventType.SCENARIO_RISK_ASSESSED,
            resource_id=str(scenario.scenario_id),
            outcome=risk_assessment.risk_level.value,
            detail=f"Risk level: {risk_assessment.risk_level.value} (advisory-only)",
        )
    )

    # --- Step 6: Human review record ---
    review_record = ReviewRecord(scenario_id=scenario.scenario_id)
    review_record.transition(ReviewState.UNDER_REVIEW, reviewer_id=actor_id)

    audit_log.append(
        AuditEntry.create(
            tenant_id=tenant_id,
            actor_id=actor_id,
            event_type=AuditEventType.REVIEW_OPENED,
            resource_id=str(scenario.scenario_id),
            outcome="UNDER_REVIEW",
            detail="Demo review opened",
        )
    )

    return DemoScenarioResult(
        tenant_id=tenant_id,
        tle_a=tle_a,
        tle_b=tle_b,
        scenario=scenario,
        screening_result=screening_result,
        risk_assessment=risk_assessment,
        review_record=review_record,
        audit_log=audit_log,
    )
