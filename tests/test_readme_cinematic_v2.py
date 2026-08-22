"""Second-generation cinematic README presentation contracts."""

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = (
    ROOT / "docs/assets/ailora-connected-worlds.svg",
    ROOT / "docs/assets/ailora-technology-rocket.svg",
    ROOT / "docs/assets/ailora-evidence-constellation.svg",
    ROOT / "docs/assets/bob-agent-portrait.svg",
    ROOT / "docs/assets/swagger-demo-stage.svg",
    ROOT / "docs/assets/project-gallery-stage.svg",
)


def test_v2_visual_assets_are_valid_substantial_svg() -> None:
    for asset in ASSETS:
        assert asset.is_file()
        assert asset.stat().st_size > 1_500
        ElementTree.parse(asset)


def test_three_new_cinematic_chapters_are_embedded() -> None:
    source = README.read_text(encoding="utf-8")
    required = (
        "## Connected Worlds",
        "docs/assets/ailora-connected-worlds.svg",
        "## Beyond the Horizon",
        "docs/assets/ailora-technology-rocket.svg",
        "## Evidence Constellation",
        "docs/assets/ailora-evidence-constellation.svg",
    )
    for value in required:
        assert value in source


def test_demo_and_four_frame_gallery_slots_are_explicit() -> None:
    source = README.read_text(encoding="utf-8")
    assert "30-Second Swagger Demo" in source
    assert "docs/assets/swagger-demo-stage.svg" in source
    assert "## Project Visual Gallery" in source
    assert "docs/assets/project-gallery-stage.svg" in source
    for label in ("GitHub", "Render", "Swagger", "Project Workspace"):
        assert label in source


def test_bob_portrait_is_inside_bob_section() -> None:
    source = README.read_text(encoding="utf-8")
    bob_start = source.index("## Bob Engineering Agent")
    roadmap_start = source.index("## Roadmap", bob_start)
    bob_section = source[bob_start:roadmap_start]
    assert "docs/assets/bob-agent-portrait.svg" in bob_section
    assert "Bob Agent Portrait" in bob_section


def test_v2_truth_and_media_boundaries_are_explicit() -> None:
    source = README.read_text(encoding="utf-8")
    assert "DEMO RECORDING SLOT" in source
    assert "MEDIA PLACEHOLDERS" in source
    assert "not evidence of production authorization" in source
    assert "NASA live data remains NOT ACTIVATED" in source
    assert ("Oya" in source) and (("PLANNED" in source) or ("planned" in source.lower()) or ("DISABLED" in source) or ("disabled" in source.lower()) or ("pending" in source.lower()) or ("NOT CURRENTLY IMPLEMENTED" in source) or ("library-agent" in source.lower()))
