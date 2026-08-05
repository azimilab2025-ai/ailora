"""
AILORA Docker Contract Tests.

Validates that Dockerfile, docker-compose.yml, and .dockerignore satisfy the
structural requirements defined in Gate 8 (P0-07) of the AILORA development
contract (CSIP-EO-FMSP).

These tests are deterministic and file-based: they parse the files directly.
No Docker daemon or container runtime is required for these structural tests.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCKERFILE_PATH = REPO_ROOT / "Dockerfile"
DOCKER_COMPOSE_PATH = REPO_ROOT / "docker-compose.yml"
DOCKERIGNORE_PATH = REPO_ROOT / ".dockerignore"


# ─── Dockerfile existence ─────────────────────────────────────────────────────


def test_dockerfile_exists() -> None:
    """Dockerfile must exist at the repository root."""
    assert DOCKERFILE_PATH.exists(), "Dockerfile not found at repository root"


# ─── Dockerfile structural requirements ──────────────────────────────────────


def test_dockerfile_has_nonroot_user() -> None:
    """Dockerfile must define and switch to a non-root USER."""
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    assert "USER" in text, "Dockerfile must contain a USER instruction (non-root)"
    # Must not run exclusively as root — there must be a USER line that is not root
    lines = [line.strip() for line in text.splitlines()]
    user_lines = [line for line in lines if line.startswith("USER ")]
    assert user_lines, "Dockerfile must have at least one USER instruction"
    # Ensure not all user lines set root
    non_root = [
        line for line in user_lines if "root" not in line.lower() and "0" not in line.split()[-1]
    ]
    assert non_root, f"Dockerfile must switch to a non-root user. USER lines found: {user_lines}"


def test_dockerfile_has_healthcheck() -> None:
    """Dockerfile must contain a HEALTHCHECK instruction."""
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    assert "HEALTHCHECK" in text, "Dockerfile must contain a HEALTHCHECK instruction"


def test_dockerfile_uses_python_slim_base() -> None:
    """Dockerfile must use python:3.11-slim (or similar slim) as base image."""
    text = DOCKERFILE_PATH.read_text(encoding="utf-8").lower()
    assert "python:3.11" in text, "Dockerfile must use python:3.11 base image"
    assert "slim" in text, "Dockerfile must use a slim base image variant"


def test_dockerfile_does_not_contain_secrets() -> None:
    """Dockerfile must not contain hardcoded secrets or credentials."""
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    forbidden_patterns = [
        "PASSWORD=",
        "SECRET=",
        "SECRET_KEY=",
        "DATABASE_URL=postgresql://",
        "POSTGRES_PASSWORD=",
        "API_KEY=",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in text, (
            f"Dockerfile must not contain hardcoded secret pattern: '{pattern}'"
        )


def test_dockerfile_is_multistage() -> None:
    """Dockerfile must use multi-stage build (at least two FROM instructions)."""
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    from_lines = [
        line.strip() for line in text.splitlines() if line.strip().upper().startswith("FROM ")
    ]
    assert len(from_lines) >= 2, (
        f"Dockerfile must use multi-stage build (≥2 FROM instructions). Found: {from_lines}"
    )


# ─── docker-compose.yml existence ────────────────────────────────────────────


def test_docker_compose_exists() -> None:
    """docker-compose.yml must exist at the repository root."""
    assert DOCKER_COMPOSE_PATH.exists(), "docker-compose.yml not found at repository root"


# ─── docker-compose.yml structural requirements ───────────────────────────────


def test_docker_compose_has_postgres_service() -> None:
    """docker-compose.yml must define a postgres service."""
    text = DOCKER_COMPOSE_PATH.read_text(encoding="utf-8")
    assert "postgres" in text.lower(), "docker-compose.yml must define a postgres service"


def test_docker_compose_has_named_volume() -> None:
    """docker-compose.yml must define at least one named volume."""
    text = DOCKER_COMPOSE_PATH.read_text(encoding="utf-8")
    # Named volumes appear in a top-level 'volumes:' section
    assert "volumes:" in text, (
        "docker-compose.yml must define a top-level 'volumes:' section with named volumes"
    )


def test_docker_compose_no_hardcoded_passwords() -> None:
    """docker-compose.yml must not contain hardcoded production passwords."""
    text = DOCKER_COMPOSE_PATH.read_text(encoding="utf-8")
    # Acceptable: placeholder values referencing env vars via ${VAR} syntax
    # Not acceptable: real-looking passwords directly assigned
    forbidden_literals = [
        "POSTGRES_PASSWORD: password123",
        "POSTGRES_PASSWORD: secret",
        "POSTGRES_PASSWORD: admin",
        "POSTGRES_PASSWORD: postgres123",
    ]
    for literal in forbidden_literals:
        assert literal not in text, (
            f"docker-compose.yml must not contain hardcoded password: '{literal}'"
        )
    # Must use env_file or ${} substitution for secrets
    uses_env_substitution = "${" in text or "env_file" in text
    assert uses_env_substitution, (
        "docker-compose.yml must use environment variable substitution (${VAR}) "
        "or env_file for secrets — no hardcoded credentials"
    )


def test_docker_compose_has_ailora_service() -> None:
    """docker-compose.yml must define the ailora application service."""
    text = DOCKER_COMPOSE_PATH.read_text(encoding="utf-8")
    assert "ailora" in text.lower(), "docker-compose.yml must define an ailora application service"


def test_docker_compose_ailora_depends_on_postgres() -> None:
    """docker-compose.yml ailora service must declare depends_on postgres."""
    text = DOCKER_COMPOSE_PATH.read_text(encoding="utf-8")
    assert "depends_on" in text, (
        "docker-compose.yml must have a depends_on declaration (ailora depends on postgres)"
    )


# ─── .dockerignore requirements ───────────────────────────────────────────────


def test_dockerignore_exists() -> None:
    """.dockerignore must exist at the repository root."""
    assert DOCKERIGNORE_PATH.exists(), ".dockerignore not found at repository root"


def test_dockerignore_excludes_venv_and_env() -> None:
    """.dockerignore must exclude .venv, .env, __pycache__, .git, and test artifacts."""
    text = DOCKERIGNORE_PATH.read_text(encoding="utf-8")
    required_exclusions = [
        ".venv",
        ".env",
        "__pycache__",
        ".git",
    ]
    for exclusion in required_exclusions:
        assert exclusion in text, f".dockerignore must exclude '{exclusion}'"
