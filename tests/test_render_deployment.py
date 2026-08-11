"""Contracts for the Render Blueprint and provider database URL."""

from pathlib import Path

import yaml

from ailora.config import Settings

ROOT = Path(__file__).resolve().parents[1]


def _blueprint() -> dict[str, object]:
    return yaml.safe_load((ROOT / "render.yaml").read_text())


def test_render_blueprint_provisions_web_and_postgres() -> None:
    blueprint = _blueprint()
    services = blueprint["services"]
    databases = blueprint["databases"]

    assert isinstance(services, list)
    assert services[0]["name"] == "ailora"
    assert isinstance(databases, list)
    assert databases[0]["name"] == "ailora-postgres"
    assert databases[0]["databaseName"] == "ailora_db"


def test_render_database_url_references_managed_postgres() -> None:
    service = _blueprint()["services"][0]
    env_vars = {item["key"]: item for item in service["envVars"]}

    assert env_vars["AILORA_DATABASE_URL"]["fromDatabase"] == {
        "name": "ailora-postgres",
        "property": "connectionString",
    }


def test_render_runtime_and_start_contract() -> None:
    service = _blueprint()["services"][0]
    env_vars = {item["key"]: item for item in service["envVars"]}

    assert env_vars["PYTHON_VERSION"]["value"].startswith("3.11.")
    assert service["buildCommand"] == "uv sync --no-dev --frozen"
    assert "uv run alembic upgrade head" in service["startCommand"]
    assert "uv run uvicorn" in service["startCommand"]
    assert service["healthCheckPath"] == "/health/live"
    assert service["autoDeployTrigger"] == "off"


def test_render_secret_is_generated_not_committed() -> None:
    service = _blueprint()["services"][0]
    env_vars = {item["key"]: item for item in service["envVars"]}

    assert env_vars["AILORA_SECRET_KEY"] == {
        "key": "AILORA_SECRET_KEY",
        "generateValue": True,
    }


def test_render_postgres_url_uses_psycopg_v3(monkeypatch: object) -> None:
    monkeypatch.setenv(  # type: ignore[attr-defined]
        "AILORA_DATABASE_URL",
        "postgresql://user:password@db.internal/ailora_db",
    )

    assert Settings().database_url == ("postgresql+psycopg://user:password@db.internal/ailora_db")
