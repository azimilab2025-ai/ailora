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
    """Author section must be the last substantive (##) section."""
    heading_lines = [
        (i, line)
        for i, line in enumerate(readme_lines)
        if line.startswith("## ") or line.startswith("# ")
    ]
    assert heading_lines, "No headings found in README.md"
    last_heading_text = heading_lines[-1][1]
    assert "Author" in last_heading_text, (
        f"The last heading in README.md is '{last_heading_text}', expected 'Author'"
    )


# ─── No fabricated operational claims ────────────────────────────────────────

PROHIBITED_CAPABILITY_PHRASES = [
    "execute-maneuver",
    "send-command",
    "uplink",
    "telecommand",
]


@pytest.mark.parametrize("phrase", PROHIBITED_CAPABILITY_PHRASES)
def test_no_fabricated_operational_claim(phrase: str, readme_text: str) -> None:
    """README must not contain prohibited operational capability claims."""
    lower_text = readme_text.lower()
    # Allow only in safety/scope/prohibition sections where it's explicitly denied
    # We check for the phrase appearing as a positive capability claim by looking
    # for it outside of "prohibited", "permanently", "out of scope", "denied" context.
    phrase_lower = phrase.lower()
    idx = lower_text.find(phrase_lower)
    while idx != -1:
        # Look at the surrounding paragraph (300 chars before/after)
        context = lower_text[max(0, idx - 300) : idx + len(phrase_lower) + 300]
        is_denial = any(
            word in context
            for word in [
                "prohibited",
                "permanently",
                "out of scope",
                "denied",
                "not",
                "no ",
                "never",
            ]
        )
        assert is_denial, (
            f"Phrase '{phrase}' appears as a positive capability claim in README.md. "
            f"Context: ...{context}..."
        )
        idx = lower_text.find(phrase_lower, idx + 1)


# ─── Oya must only appear as planned/not implemented ─────────────────────────


def test_oya_only_planned(readme_text: str) -> None:
    """Oya section must carry PLANNED / NOT CURRENTLY IMPLEMENTED qualifier.

    We locate the containing section (bounded by the nearest preceding ##
    heading) and verify the qualifier appears somewhere in that section.
    """
    if "Oya" not in readme_text:
        return  # Oya not mentioned is acceptable

    lower = readme_text.lower()
    oya_idx = lower.find("oya")
    while oya_idx != -1:
        # Expand context to the surrounding section (~500 chars before/after)
        context = lower[max(0, oya_idx - 500) : oya_idx + 500]
        denial_words = [
            "planned",
            "not currently implemented",
            "not implemented",
            "not authorized",
            "no oya",
            "prohibited",
            "not yet",
        ]
        is_safe = any(word in context for word in denial_words)
        assert is_safe, (
            f"'Oya' appears without a PLANNED/NOT CURRENTLY IMPLEMENTED qualifier. "
            f"Context: ...{context}..."
        )
        oya_idx = lower.find("oya", oya_idx + 1)


# ─── No invented live URLs ────────────────────────────────────────────────────

INVENTED_URL_PATTERNS = [
    "ailora.azimi",
    "ailora.io",
    "ailora.app",
    "ailora.dev",
    "ailora.ai",
]


@pytest.mark.parametrize("url_pattern", INVENTED_URL_PATTERNS)
def test_no_invented_live_url(url_pattern: str, readme_text: str) -> None:
    """README must not contain invented live deployment URLs for undeployed resources."""
    assert url_pattern not in readme_text.lower(), (
        f"Invented live URL pattern '{url_pattern}' found in README.md"
    )


# ─── Prompt 06 boundary statement ────────────────────────────────────────────


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
