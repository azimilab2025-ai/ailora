import re
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_ci_has_explicit_least_privilege_permissions() -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text()
    assert "permissions:\n  contents: read" in text
    assert "timeout-minutes:" in text


def test_all_ci_actions_are_pinned_to_commit_sha() -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text()
    uses = re.findall(r"uses:\s+[^@\s]+@([^\s#]+)", text)
    assert uses
    assert all(re.fullmatch(r"[0-9a-f]{40}", value) for value in uses)


def test_coverage_floor_is_defensible_and_nonzero() -> None:
    text = (ROOT / "pyproject.toml").read_text()
    assert "--cov-fail-under=85" in text
    assert "fail_under = 85" in text


def test_ci_contains_local_security_and_artifact_gates() -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text()
    for marker in ("ruff check", "generate_sbom.py", "uv build", "uv lock --check"):
        assert marker in text
