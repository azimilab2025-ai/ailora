"""Final visual redesign contracts for Author, Oya, and Roadmap."""

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = (
    ROOT / "docs/assets/author-command-deck.svg",
    ROOT / "docs/assets/ailora-capability-hive.svg",
    ROOT / "docs/assets/oya-plan-dag.svg",
    ROOT / "docs/assets/oya-safety-orbit.svg",
    ROOT / "docs/assets/roadmap-trajectory.svg",
)


def section(source: str, heading: str) -> str:
    start = source.index(heading)
    next_heading = source.find("\n## ", start + len(heading))
    return source[start:] if next_heading == -1 else source[start:next_heading]


def test_all_visuals_are_valid_substantial_svg() -> None:
    for asset in ASSETS:
        assert asset.is_file()
        assert asset.stat().st_size > 2_000
        ElementTree.parse(asset)


def test_author_is_a_dedicated_visual_command_deck() -> None:
    source = README.read_text(encoding="utf-8")
    author = section(source, "## Author")
    assert "docs/assets/author-command-deck.svg" in author
    assert "AMIN AZIMI" in author
    assert "AI ARCHITECT" in author
    assert "End-to-End System Architecture" in author
    assert "| Field | Value |" not in author


def test_oya_section_is_visual_sourced_and_truthful() -> None:
    source = README.read_text(encoding="utf-8")
    assert "docs/assets/ailora-capability-hive.svg" in source
    assert "docs/assets/oya-plan-dag.svg" in source
    assert "docs/assets/oya-safety-orbit.svg" in source
    assert "https://github.com/OyaAIProd.png" in source
    assert "https://github.com/OyaAIProd/oya" in source
    assert "bun add oyadotai zod" in source
    assert "PLANNED / NOT CURRENTLY IMPLEMENTED / DISABLED" in source
    assert "No zero-error guarantee is claimed" in source


def test_roadmap_is_a_visual_trajectory_not_a_table() -> None:
    source = README.read_text(encoding="utf-8")
    roadmap = section(source, "## Roadmap")
    assert "docs/assets/roadmap-trajectory.svg" in roadmap
    roadmap_visual = (ROOT / "docs/assets/roadmap-trajectory.svg").read_text(encoding="utf-8")
    assert "PHASE 0" in roadmap_visual and "PHASE 7" in roadmap_visual
    assert "| Phase |" not in roadmap


def test_target_sections_have_no_legacy_markdown_tables() -> None:
    source = README.read_text(encoding="utf-8")
    author = section(source, "## Author")
    roadmap = section(source, "## Roadmap")
    oya_start = source.index("Future Integration Roadmap: Oya Voice AI")
    oya_end = source.find("\n## ", oya_start)
    oya = source[oya_start:] if oya_end == -1 else source[oya_start:oya_end]
    assert "|---" not in author
    assert "|---" not in roadmap
    assert "|---" not in oya
