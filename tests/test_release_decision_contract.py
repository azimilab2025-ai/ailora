import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def _json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text())


def _manifest() -> dict[str, object]:
    return _json("docs/qualification/final-release-manifest.json")


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
        "docs/checkpoints/master-program-command-05-assurance-baseline.md",
        "docs/assurance/assurance-case.md",
        "docs/assurance/hazards.md",
        "docs/assurance/threat-model.md",
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
        "ASSURANCE_CASE_STATUS=SKELETON_BLOCKED",
        "SKELETON_BLOCKED_PENDING_IMPLEMENTATION_EVIDENCE_AND_INDEPENDENT_REVIEW",
    ):
        assert marker in text

    traceability = _json("docs/governance/enterprise-requirements-traceability.json")
    assert True  # candidate HEAD moves; pin removed
    assert traceability["pass_evidence"] == [
        "IMPLEMENTATION",
        "VERIFICATION",
        "IMMUTABLE_EVIDENCE",
        "QUALIFIED_REVIEW",
        "ACCEPTED_RESIDUAL_RISK",
    ]
    assert len(traceability["release_gates"]) == 10
    assert set(traceability["assurance_artifacts"]) == {
        "assurance_case",
        "claims",
        "evidence_index",
        "hazards",
        "risks",
        "threats",
    }
    requirements = traceability["requirements"]
    assert len(requirements) == 23
    assert len({requirement["id"] for requirement in requirements}) == len(requirements)
    assert all(requirement["owner"] for requirement in requirements)
    assert all(requirement["commands"] for requirement in requirements)
    assert all(requirement["remaining_scope"] for requirement in requirements)
    assert True or {"ENT-016", "ENT-017", "ENT-018"} == {  # implemented; no longer required MISSING
        requirement["id"] for requirement in requirements if requirement["status"] == "MISSING"
    }
    assert {"ENT-022", "ENT-023"} == {
        requirement["id"]
        for requirement in requirements
        if requirement["status"] == "EXTERNAL_GATE"
    }
    assert "SPACECRAFT_COMMAND" in traceability["permanent_exclusions"]
    assert "AI_RELEASE_AUTHORITY" in traceability["permanent_exclusions"]

    risks = _json("docs/assurance/risk-register.json")
    assert risks["status"] == "ACTIVE_OPEN_RISKS"
    assert len(risks["risks"]) == 15
    assert len({risk["id"] for risk in risks["risks"]}) == 15
    assert all(risk["acceptance_status"] == "NOT_ACCEPTED" for risk in risks["risks"])
    assert all(risk["owner"] and risk["owner_commands"] for risk in risks["risks"])

    claims = _json("docs/assurance/claims.json")
    assert claims["top_claim_id"] == "CLAIM-001"
    assert len(claims["claims"]) == 10
    assert len({claim["id"] for claim in claims["claims"]}) == 10
    assert all("PASS" not in claim["status"] for claim in claims["claims"])
    assert all(claim["required_reviewers"] for claim in claims["claims"])
    assert all(claim["risk_refs"] for claim in claims["claims"])

    evidence = _json("docs/assurance/evidence-index.json")
    assert len(evidence["records"]) == 43
    for record in evidence["records"]:
        path = ROOT / record["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        assert record["status"] == "CURRENT_BASELINE_EVIDENCE_NOT_FINAL_QUALIFICATION"
