"""
AILORA P1-05: CI/CD Baseline Contract Tests.

Validates that the GitHub Actions workflow file is structurally correct
and meets the AILORA CI contract:
- Workflow file exists and is valid YAML structure.
- Required steps are present: install, lint, format-check, typecheck, test.
- No secrets are hardcoded in the workflow.
- Workflow does not perform deployments (production-gate not authorized).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def test_ci_workflow_exists() -> None:
    """.github/workflows/ci.yml must exist."""
    assert CI_WORKFLOW.exists(), ".github/workflows/ci.yml not found"


def test_ci_workflow_parseable_yaml() -> None:
    """CI workflow must be valid YAML."""
    import yaml  # type: ignore[import-untyped]
    content = CI_WORKFLOW.read_text(encoding="utf-8")
    doc = yaml.safe_load(content)
    assert doc is not None, "ci.yml must not be empty"
    assert isinstance(doc, dict), "ci.yml must parse to a YAML mapping"


def test_ci_workflow_has_push_and_pr_triggers() -> None:
    """Workflow must trigger on push and pull_request to main."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "push" in text, "CI workflow must trigger on push"
    assert "pull_request" in text, "CI workflow must trigger on pull_request"


def test_ci_workflow_uses_python_311() -> None:
    """Workflow must configure Python 3.11."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "3.11" in text, "CI workflow must use Python 3.11"


def test_ci_workflow_has_uv_install() -> None:
    """Workflow must install dependencies via uv."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "uv" in text.lower(), "CI workflow must use uv for dependency installation"


def test_ci_workflow_has_lint_step() -> None:
    """Workflow must include a ruff lint step."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "ruff check" in text, "CI workflow must run 'ruff check'"


def test_ci_workflow_has_format_check_step() -> None:
    """Workflow must include a ruff format check step."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "ruff format --check" in text, "CI workflow must run 'ruff format --check'"


def test_ci_workflow_has_typecheck_step() -> None:
    """Workflow must include a mypy type-check step."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "mypy" in text, "CI workflow must run mypy type-checking"


def test_ci_workflow_has_test_step() -> None:
    """Workflow must include a pytest test step."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "pytest" in text, "CI workflow must run pytest"


def test_ci_workflow_no_hardcoded_secrets() -> None:
    """CI workflow must not contain hardcoded secrets or credentials."""
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    # ${{ secrets.X }} is acceptable; raw values are not
    forbidden_patterns = [
        "password: ",
        "secret_key: ",
        "api_key: ",
        "DATABASE_URL: postgresql://",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in text.lower(), (
            f"CI workflow must not contain hardcoded credential: '{pattern}'"
        )


def test_ci_workflow_no_deploy_steps() -> None:
    """CI workflow must not contain deployment step commands."""
    import yaml  # type: ignore[import-untyped]
    doc = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
    # Collect all 'run' step commands from all jobs
    run_commands: list[str] = []
    for job in (doc.get("jobs") or {}).values():
        for step in job.get("steps", []):
            run_cmd = step.get("run", "")
            if run_cmd:
                run_commands.append(run_cmd.lower())
    # None of the run commands should perform production deploys
    prohibited_in_run = ["heroku", "fly.io", "render deploy", "kubectl apply", "docker push"]
    for cmd in run_commands:
        for forbidden in prohibited_in_run:
            assert forbidden not in cmd, (
                f"CI workflow run step must not perform: '{forbidden}'"
            )
