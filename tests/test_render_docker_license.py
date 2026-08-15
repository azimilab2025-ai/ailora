"""Docker license build-order regression tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "Dockerfile"


def test_license_is_copied_before_uv_sync() -> None:
    source = DOCKERFILE.read_text(encoding="utf-8")
    copy_instruction = "COPY pyproject.toml uv.lock README.md LICENSE ./"
    sync_instruction = "UV_PROJECT_ENVIRONMENT=/opt/venv uv sync --no-dev --frozen"

    assert copy_instruction in source, (
        "LICENSE must be copied before uv sync because pyproject.toml "
        "declares LICENSE as project metadata"
    )
    assert sync_instruction in source
    assert source.index(copy_instruction) < source.index(sync_instruction)


def test_license_exists_and_is_not_dockerignored() -> None:
    assert (ROOT / "LICENSE").is_file()

    ignored_entries = {
        line.strip()
        for line in (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    assert "LICENSE" not in ignored_entries
    assert "/LICENSE" not in ignored_entries
