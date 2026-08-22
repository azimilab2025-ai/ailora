import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "docs/qualification/final-release-manifest.json"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text())


def test_final_manifest_identity_metrics_and_scope() -> None:
    manifest = _manifest()
    assert manifest["schema_version"] == 1
    assert isinstance(manifest.get("artifact_id"), str) and len(manifest.get("artifact_id", "")) > 0
    assert isinstance(manifest.get("source_commit"), str) and len(manifest.get("source_commit", "")) >= 7
    assert manifest["decision"]["verified_scope"] == "ENGINEERING_PRODUCTION_CANDIDATE"
    assert manifest["decision"]["production_release"] == "BLOCKED_PENDING_P0_GATES"
    assert manifest["decision"]["risk_semantics"] == (
        "DISTANCE_BASED_PROXIMITY_SEVERITY_NOT_COLLISION_PROBABILITY"
    )
    assert isinstance(manifest.get("metrics"), dict)


def test_every_evidence_digest_matches_repository_bytes() -> None:
    evidence = _manifest()["evidence"]
    assert len(evidence) == 30
    paths = [item["path"] for item in evidence]
    assert paths == sorted(paths) and len(paths) == len(set(paths))
    for item in evidence:
        path = ROOT / item["path"]
        assert path.is_file(), item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]


def test_manifest_actions_are_all_non_operational() -> None:
    actions = _manifest()["actions"]
    assert actions and set(actions.values()) == {"NONE"}
