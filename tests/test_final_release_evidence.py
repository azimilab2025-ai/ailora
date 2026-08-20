"""Focused tests for COMMAND-30 final release evidence surface (ENT-001/002 local part)."""

from __future__ import annotations

import pytest


def test_residual_risk_record_accepts_valid() -> None:
    from ailora.recovery.qualification import ResidualRiskRecord

    r = ResidualRiskRecord(
        risk_id="RR-001",
        severity="MEDIUM",
        acceptance_status="ACCEPTED",
        evidence_digest="a" * 64,
    )
    assert r.risk_id == "RR-001"
    assert r.acceptance_status == "ACCEPTED"


def test_residual_risk_record_rejects_bad_digest() -> None:
    from ailora.recovery.qualification import RecoveryContractError, ResidualRiskRecord

    with pytest.raises(RecoveryContractError):
        ResidualRiskRecord(
            risk_id="RR-002",
            severity="LOW",
            acceptance_status="DEFERRED",
            evidence_digest="short",
        )


def test_assurance_case_index_entry_accepts_valid() -> None:
    from ailora.recovery.qualification import AssuranceCaseIndexEntry

    e = AssuranceCaseIndexEntry(
        entry_id="ACE-001",
        claim_ref="CLAIM-01",
        evidence_ref="EV-01",
        coverage_status="COVERED",
    )
    assert e.coverage_status == "COVERED"


def test_release_authority_boundary_accepts_valid() -> None:
    from ailora.recovery.qualification import ReleaseAuthorityBoundary

    b = ReleaseAuthorityBoundary(
        boundary_id="RAB-001",
        human_authority_required=True,
        no_command_enforced=True,
        audit_ref="AUDIT-01",
    )
    assert b.no_command_enforced is True


def test_final_release_decision_record_accepts_valid() -> None:
    from ailora.recovery.qualification import FinalReleaseDecisionRecord

    d = FinalReleaseDecisionRecord(
        decision_id="FRD-001",
        residual_risks=("RR-001",),
        assurance_index_digest="b" * 64,
        authority_ack="OWNER-ACK",
        outcome="ADVISORY_ONLY",
    )
    assert d.outcome == "ADVISORY_ONLY"
