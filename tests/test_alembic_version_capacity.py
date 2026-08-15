from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).parents[1]
VERSIONS = ROOT / "alembic/versions"
BRIDGE = VERSIONS / "0009a_expand_alembic_version.py"
SUCCESSOR = VERSIONS / "0010_space_data_provider_governance.py"


def _revision_values(path: Path) -> dict[str, str | None]:
    tree = ast.parse(path.read_text(), filename=str(path))
    values: dict[str, str | None] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if not isinstance(target, ast.Name) or target.id not in {"revision", "down_revision"}:
                continue
            if isinstance(node.value, ast.Constant):
                values[target.id] = node.value.value
    return values


def test_short_bridge_is_inserted_before_long_revision() -> None:
    bridge = _revision_values(BRIDGE)
    successor = _revision_values(SUCCESSOR)
    assert bridge == {
        "revision": "0009a_expand_version",
        "down_revision": "0009_space_data_contracts",
    }
    assert len(bridge["revision"] or "") <= 32
    assert successor["revision"] == "0010_space_data_provider_governance"
    assert successor["down_revision"] == bridge["revision"]


def test_bridge_expands_postgres_version_column_before_long_revision() -> None:
    source = BRIDGE.read_text()
    assert 'dialect.name == "postgresql"' in source
    assert "op.alter_column(" in source
    assert '"alembic_version"' in source
    assert '"version_num"' in source
    assert "sa.String(length=64)" in source


def test_bridge_downgrade_restores_original_capacity() -> None:
    source = BRIDGE.read_text()
    assert source.count("sa.String(length=32)") >= 2
    assert source.count("sa.String(length=64)") >= 2
