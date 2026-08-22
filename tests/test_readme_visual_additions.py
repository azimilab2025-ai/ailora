"""Contracts for the additive Mission Control and aerospace blueprint visuals."""

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MISSION = ROOT / "docs/assets/ailora-mission-control-strip.svg"
BLUEPRINT = ROOT / "docs/assets/ailora-aerospace-blueprint.svg"
ASSETS = (MISSION, BLUEPRINT)
SVG = "{http://www.w3.org/2000/svg}"


def test_visual_assets_are_valid_accessible_svg() -> None:
    for asset in ASSETS:
        assert asset.is_file()
        root = ElementTree.parse(asset).getroot()
        assert root.tag == f"{SVG}svg"
        assert root.attrib["role"] == "img"
        assert root.attrib["aria-labelledby"]
        assert root.find(f"{SVG}title") is not None
        assert root.find(f"{SVG}desc") is not None


def test_visual_assets_are_substantial_and_responsive() -> None:
    for asset in ASSETS:
        assert asset.stat().st_size > 5_000
        root = ElementTree.parse(asset).getroot()
        assert root.attrib["viewBox"]
        assert root.attrib["width"] == "1440"


def test_visual_assets_are_self_contained_and_script_free() -> None:
    forbidden = {"script", "foreignObject", "animate", "animateMotion", "set", "image"}
    for asset in ASSETS:
        root = ElementTree.parse(asset).getroot()
        local_names = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
        assert forbidden.isdisjoint(local_names)
        for element in root.iter():
            assert not any(key.rsplit("}", 1)[-1] == "href" for key in element.attrib)


def test_visual_assets_support_dark_and_light_color_schemes() -> None:
    for asset in ASSETS:
        source = asset.read_text(encoding="utf-8")
        assert "@media (prefers-color-scheme: light)" in source


def test_readme_adds_visuals_without_replacing_inspectable_content() -> None:
    source = README.read_text(encoding="utf-8")
    assert source.count("docs/assets/ailora-mission-control-strip.svg") == 1
    assert source.count("docs/assets/ailora-aerospace-blueprint.svg") == 1
    assert "| Control-plane signal | Verified state |" in source
    assert "```mermaid\ngraph TB" in source
    assert "20 OpenAPI paths" in source
    assert ("1053" in source) or ("passed" in source.lower())
    assert "87.56% against an enforced 85% floor" in source


def test_visual_copy_preserves_verified_status_and_safety_boundaries() -> None:
    mission = " ".join(
        text.strip() for text in ElementTree.parse(MISSION).getroot().itertext() if text.strip()
    )
    blueprint = " ".join(
        text.strip() for text in ElementTree.parse(BLUEPRINT).getroot().itertext() if text.strip()
    )
    for token in (
        "700 PASS",
        "87.56%",
        "20 PATHS",
        "CELESTRAK",
        "E2E DEFERRED",
        "NASA INTEGRATION",
        "NOT ACTIVE",
        "HUMAN AUTHORITY",
        "NO SPACECRAFT COMMAND",
    ):
        assert token in mission
    for token in (
        "ORBITAL INTELLIGENCE",
        "PHYSICS LAYER",
        "AI ADVISORY",
        "EVIDENCE CHAIN",
        "HUMAN AUTHORITY",
        "PRODUCTION E2E DEFERRED",
        "NO TELECOMMAND",
        "NO AUTONOMOUS MANEUVER",
    ):
        assert token in blueprint
