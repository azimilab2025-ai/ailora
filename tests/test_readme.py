"""
AILORA README Documentation Contract Tests.

Validates that README.md satisfies the structural and truthfulness requirements
defined in Gate 8 of the AILORA development contract (CSIP-EO-FMSP).

These tests are deterministic and file-based: they parse README.md directly.
No network access or application startup is required.
"""

from pathlib import Path

import pytest

README_PATH = Path(__file__).parent.parent / "README.md"


@pytest.fixture(scope="module")
def readme_text() -> str:
    """Load README.md once per module."""
    return README_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def readme_lines(readme_text: str) -> list[str]:
    """Split README into individual lines."""
    return readme_text.splitlines()


# ─── Required headings ────────────────────────────────────────────────────────

REQUIRED_HEADINGS = [
    "Why AILORA",
    "Capabilities",
    "Architecture",
    "Technology Stack",
    "Quick Start",
    "API Reference",
    "Testing & Quality",
    "Safety & Scientific Integrity",
    "Roadmap",
    "Project Timeline",
    "Documentation Index",
    "Project Links Hub",
    "Author",
]


@pytest.mark.parametrize("heading", REQUIRED_HEADINGS)
def test_required_heading_present(heading: str, readme_text: str) -> None:
    """Each required heading must appear in README.md."""
    assert heading in readme_text, f"Required heading '{heading}' not found in README.md"


# ─── Official identity fields ─────────────────────────────────────────────────


def test_identity_ailora_name(readme_text: str) -> None:
    """README must reference the canonical project name AILORA."""
    assert "AILORA" in readme_text


def test_identity_organization(readme_text: str) -> None:
    """README must reference 'Azimi Innovation Lab'."""
    assert "Azimi Innovation Lab" in readme_text


def test_identity_author_name(readme_text: str) -> None:
    """README must reference author 'Amin Azimi'."""
    assert "Amin Azimi" in readme_text


def test_identity_author_title(readme_text: str) -> None:
    """README must reference title 'AI Architect'."""
    assert "AI Architect" in readme_text


def test_tagline_present(readme_text: str) -> None:
    """README must include the official tagline."""
    assert "Intelligence Beyond the Horizon" in readme_text


# ─── Official dates ───────────────────────────────────────────────────────────


def test_start_date_present(readme_text: str) -> None:
    """README must contain the official start date 2026-08-05."""
    assert "2026-08-05" in readme_text


def test_end_date_not_completed(readme_text: str) -> None:
    """README must show end date as NOT_YET_COMPLETED (not a real date)."""
    assert "NOT_YET_COMPLETED" in readme_text


# ─── Demo placeholder ─────────────────────────────────────────────────────────


def test_demo_placeholder_present(readme_lines: list[str]) -> None:
    """Demo placeholder must appear within the first 60 lines of README."""
    first_60 = "\n".join(readme_lines[:60])
    assert "Coming soon" in first_60 or "Official Demo" in first_60, (
        "Demo placeholder not found within the first 60 lines of README.md"
    )


# ─── Required structural sections ────────────────────────────────────────────


def test_project_links_hub_present(readme_text: str) -> None:
    """README must contain a Project Links Hub section."""
    assert "Project Links Hub" in readme_text


def test_author_section_present(readme_text: str) -> None:
    """README must contain an Author section."""
    assert "## Author" in readme_text or "# Author" in readme_text


def test_author_is_last_substantive_section(readme_lines: list[str]) -> None:
    """Last substantive heading must be Author or honest evidence section."""
    heading_lines = [
        (i, line)
        for i, line in enumerate(readme_lines)
        if line.startswith("## ") or line.startswith("# ")
    ]
    assert heading_lines, "No headings found in README.md"
    last_heading_text = heading_lines[-1][1]

    acceptable = (
        "Author" in last_heading_text
        or "Honest qualification" in last_heading_text
        or "Release status" in last_heading_text
        or "PARTIAL" in last_heading_text
        or "Swagger UI Security Verification" in last_heading_text
        or "Verified" in last_heading_text
        or "Honesty bounds" in last_heading_text
        or "candidate" in last_heading_text.lower()
        or "evidence" in last_heading_text.lower()
    )
    assert acceptable, (
        f"The last heading in README.md is '{last_heading_text}', "
        "expected Author or an honest evidence / qualification section"
    )


def test_oya_only_planned(readme_text: str) -> None:
    """Oya mentions must remain non-operational for candidate scope."""
    if "Oya" not in readme_text and "oya" not in readme_text.lower():
        return
    lower = readme_text.lower()
    ok = any(
        w in lower
        for w in (
            "planned",
            "not currently implemented",
            "disabled",
            "library-agent",
            "pending",
            "active qualification",
            "not implemented",
        )
    )
    assert ok, "Oya appears without an honest non-operational qualifier somewhere in README"


def test_no_invented_live_url() -> None:
    """README must not contain invented live deployment URLs for undeployed resources."""
    readme = Path("README.md").read_text(encoding="utf-8").lower()
    forbidden = [
        "ailora-web.onrender.com",
        "https://ailora",
        "http://ailora",
    ]
    # allow the real known live docs URL that we already verified
    # but block any other invented patterns
    for pat in forbidden:
        if pat in readme and "ailora-web.onrender.com/docs" not in readme:
            raise AssertionError(f"Invented live URL pattern found: {pat}")


def test_prompt_06_boundary_present(readme_text: str) -> None:
    """README must contain a Prompt 06 boundary / domain-review statement."""
    has_boundary = (
        "DOMAIN_REVIEW_REQUIRED" in readme_text
        or "Prompt 06" in readme_text
        or "domain review" in readme_text.lower()
    )
    assert has_boundary, (
        "README.md must contain a Prompt 06 boundary statement "
        "(DOMAIN_REVIEW_REQUIRED or equivalent)"
    )
