.PHONY: help install install-dev lint typecheck test test-cov clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install:  ## Install runtime dependencies via uv
	uv sync --no-dev

install-dev:  ## Install all dependencies including dev tools
	uv sync

lint:  ## Run ruff linter
	uv run ruff check src/ tests/

lint-fix:  ## Run ruff linter with auto-fix
	uv run ruff check --fix src/ tests/

format:  ## Run ruff formatter
	uv run ruff format src/ tests/

format-check:  ## Check formatting without changing files
	uv run ruff format --check src/ tests/

typecheck:  ## Run mypy type checker
	uv run mypy src/

test:  ## Run pytest
	uv run pytest tests/ -v

test-cov:  ## Run pytest with coverage report
	uv run pytest tests/ -v --cov=src/ailora --cov-report=term-missing

clean:  ## Remove build artefacts and caches
	rm -rf dist/ build/ .eggs/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ .coverage
