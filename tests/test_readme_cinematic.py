"""Cinematic README and Bob engineering-agent documentation contracts."""

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
HERO = ROOT / "docs/assets/ailora-cinematic-hero.svg"
BOB = ROOT / "docs/assets/bob-engineering-agent.svg"


def test_cinematic_assets_are_valid_svg() -> None:
    for asset in (HERO, BOB):
        assert asset.is_file()
        ElementTree.parse(asset)


def test_readme_references_visual_assets() -> None:
    source = README.read_text(encoding="utf-8")
    assert "docs/assets/ailora-cinematic-hero.svg" in source
    assert "docs/assets/bob-engineering-agent.svg" in source


def test_bob_agent_scope_and_boundaries() -> None:
    source = README.read_text(encoding="utf-8")
    assert "## Bob Engineering Agent" in source
    assert "Engineering copilot" in source
    assert "not a deployed runtime service" in source
    assert "cannot approve scientific results" in source
    assert "cannot execute spacecraft commands" in source


def test_live_render_links_and_truthful_status() -> None:
    source = README.read_text(encoding="utf-8")
    assert "https://ailora-web.onrender.com" in source
    assert "https://ailora-web.onrender.com/docs" in source
    assert "NASA live data" in source and "NOT ACTIVATED" in source
    assert "Oya voice service" in source and "DISABLED" in source
    assert "Human authority" in source and "REQUIRED" in source
