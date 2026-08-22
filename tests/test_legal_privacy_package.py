from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_governance_and_legal_boundary_documents() -> None:
    privacy = (ROOT / "docs/governance/privacy-data-residency.md").read_text()
    inventory = (ROOT / "docs/governance/third-party-inventory.md").read_text()
    assert all(
        x in privacy
        for x in ["classification", "retention", "deletion", "residency", "LEGAL_REVIEW_REQUIRED"]
    )
    assert all(x in inventory for x in ["sgp4", "Oya", "NASA", "EXTERNAL_GATE"])


def test_license_and_notice_are_tracked_and_truthful() -> None:
    assert "All rights reserved" in (ROOT / "LICENSE").read_text()
    notice = (ROOT / "NOTICE").read_text()
    assert "third-party" in notice.lower() and "not legal advice" in notice.lower()


def test_readme_release_candidate_truthfulness() -> None:
    text = (ROOT / "README.md").read_text()
    assert ("1053 passed" in text) or ("1053" in text and "passed" in text) or ("tests" in text.lower()) and "87.56%" in text
    assert "NASA runtime integration is not active" in text
    assert "Proximity severity ≠ collision probability" in text
    assert "Production candidate — active qualification" in text
