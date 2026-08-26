# ─── Stage 1: Builder ─────────────────────────────────────────────────────────
# Install all dependencies into a dedicated build layer.
# This stage is discarded in the final image, keeping build artefacts
# and unnecessary tooling out of the production layer.
FROM python:3.11-slim AS builder

# Prevent interactive prompts and ensure reproducible pip installs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install uv for fast, reproducible dependency resolution
RUN pip install --no-cache-dir "uv==0.12.2"

# Copy only the dependency definition files first to exploit Docker layer cache.
# Source code changes will not invalidate this layer.
# README.md and LICENSE are required by project metadata during package installation.
COPY pyproject.toml uv.lock README.md LICENSE ./

# Copy source tree — needed for the local `ailora` package editable install
COPY src/ ./src/

# Create a virtual environment and sync production dependencies only.
# UV_PROJECT_ENVIRONMENT directs uv sync to install into /opt/venv.
# --no-dev excludes test/lint extras; --frozen ensures exact lockfile versions.
RUN uv venv /opt/venv && \
    UV_PROJECT_ENVIRONMENT=/opt/venv uv sync --no-dev --frozen

# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
# Minimal runtime image — no build tools, no lock files, no secrets.
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src"

WORKDIR /app

# Create a non-root system user and group for running the application.
# UID 1001 / GID 1001 — avoids collision with common host user IDs.
RUN groupadd --gid 1001 ailora && \
    useradd --uid 1001 --gid ailora --shell /usr/sbin/nologin --no-create-home ailora

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code only — no lock files, no tests, no secrets
COPY src/ ./src/

# Copy Alembic configuration and migration scripts
COPY alembic.ini ./alembic.ini
COPY alembic/ ./alembic/

# Keep the application tree root-owned and non-writable by the runtime identity.
RUN chown -R root:root /app && chmod -R a-w /app

# Switch to the non-root user — no further root operations
USER ailora

# Expose the default application port
EXPOSE 8000

# Health check — poll the liveness endpoint every 30s
# Start period of 10s allows the application to initialise before checks begin
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" \
    || exit 1

# Default command — can be overridden in docker-compose or at runtime
CMD ["uvicorn", "ailora.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
