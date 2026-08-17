import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def _manifest() -> dict[str, object]:
    return json.loads((ROOT / "docs/qualification/final-release-manifest.json").read_text())


def test_external_gates_remain_open_and_owned() -> None:
    gates = _manifest()["external_gates"]
    assert {gate["id"] for gate in gates} == {
        "DATA-001",
        "E2E-001",
        "HA-001",
        "LEGAL-001",
        "OPS-001",
        "OYA-001",
        "SCI-001",
        "SHADOW-001",
    }
    assert all(gate["status"] == "OPEN_EXTERNAL_GATE" for gate in gates)
    assert all(gate["owner"] and gate["closure_evidence"] for gate in gates)


def test_fail_closed_decision_rejects_overclaims() -> None:
    decision = _manifest()["decision"]
    assert decision["final_status"] == "PRODUCTION_CANDIDATE_ACTIVE_QUALIFICATION"
    assert decision["controlled_provider_e2e_passed"] is False
    assert decision["no_spacecraft_command_surface"] is True
    assert decision["production_ready_claim_allowed"] is False
    assert decision["scientific_approval_claim_allowed"] is False
    assert decision["legal_compliance_claim_allowed"] is False
    assert decision["live_provider_claim_allowed"] is False
    assert decision["human_release_authority_required"] is True


def test_final_documents_preserve_truthful_boundaries() -> None:
    document_paths = (
        "docs/qualification/final-evidence-pack.md",
        "docs/governance/residual-risk-and-release-decision.md",
        "docs/checkpoints/final-program-command-20-final-evidence-checkpoint.md",
        "docs/governance/release-scope-and-authority.md",
        "docs/architecture/enterprise-adr-register.md",
        "docs/checkpoints/master-program-command-04-governance-baseline.md",
    )
    text = "\n".join((ROOT / path).read_text() for path in document_paths)
    for marker in (
        "PRODUCTION_RELEASE=BLOCKED",
        "DOMAIN_REVIEW_REQUIRED",
        "LIVE_NASA_DATA=NOT_ACTIVATED",
        "OYA_STATUS=DISABLED",
        "LEGAL_REVIEW_REQUIRED",
        "HUMAN_RELEASE_AUTHORITY=MANDATORY",
        "PRODUCTION_CANDIDATE_ACTIVE_QUALIFICATION",
        "DEFERRED_REQUIRED_BEFORE_FINAL_RELEASE",
        "Proximity severity is not collision probability",
        "No spacecraft command",
    ):
        assert marker in text

    traceability = json.loads(
        (ROOT / "docs/governance/enterprise-requirements-traceability.json").read_text()
    )
    assert traceability["baseline_commit"] == "59d0fbc55e9e1b50fe1877af382df382602ae54a"
    assert traceability["pass_evidence"] == [
        "IMPLEMENTATION",
        "VERIFICATION",
        "IMMUTABLE_EVIDENCE",
        "QUALIFIED_REVIEW",
        "ACCEPTED_RESIDUAL_RISK",
    ]
    assert len(traceability["release_gates"]) == 10
    requirements = traceability["requirements"]
    assert len(requirements) == 23
    assert len({requirement["id"] for requirement in requirements}) == len(requirements)
    assert all(requirement["owner"] for requirement in requirements)
    assert all(requirement["commands"] for requirement in requirements)
    assert all(requirement["remaining_scope"] for requirement in requirements)
    assert {"ENT-016", "ENT-017", "ENT-018"} == {
        requirement["id"] for requirement in requirements if requirement["status"] == "MISSING"
    }
    assert {"ENT-022", "ENT-023"} == {
        requirement["id"]
        for requirement in requirements
        if requirement["status"] == "EXTERNAL_GATE"
    }
    assert "SPACECRAFT_COMMAND" in traceability["permanent_exclusions"]
    assert "AI_RELEASE_AUTHORITY" in traceability["permanent_exclusions"]
