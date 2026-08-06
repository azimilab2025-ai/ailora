# AILORA — Verification Baseline

**Project:** AILORA — An Azimi Innovation Lab Orbital Intelligence System
**Author / AI Architect:** Amin Azimi
**Organisation:** Azimi Innovation Lab
**Authoritative source:** Prompts 01–15 (CSIP-EO-FMSP)
**Official project start:** 2026-08-05
**Document purpose:** Record evidence of quality-gate state at each development milestone.
                      All results are backed by actual command execution; no result is
                      fabricated or assumed.

---

## PHASE_0 — Repository and Engineering Baseline

### Gate 8 Baseline — 2026-08-05

**Work items closed:** P0-01 through P0-08
**Exit condition:** Repository, tooling, identity docs, scaffold, Docker, and documentation
contract are all operational and verified.

#### Test Results

| Suite | Collected | Passed | Failed | Notes |
|---|---|---|---|---|
| `tests/test_health.py` | 2 | 2 | 0 | Liveness + readiness probes |
| `tests/test_readme.py` | 35 | 35 | 0 | README documentation contract |
| `tests/test_docker_contracts.py` | 14 | 14 | 0 | Dockerfile / docker-compose structural contracts |
| **Total** | **51** | **51** | **0** | All tests pass |

#### Quality Gate Results

| Check | Command | Result | Notes |
|---|---|---|---|
| Ruff format | `uv run ruff format --check src/ tests/` | ✅ Pass | 11 files, all formatted |
| Ruff lint | `uv run ruff check src/ tests/` | ✅ Pass | 0 issues |
| Mypy strict | `uv run mypy src/` | ✅ Pass | 0 issues, 7 source files |
| Docker build | `docker build . -t ailora:dev` | ✅ Pass | Multi-stage, non-root, HEALTHCHECK |
| Docker Compose | `docker compose config` | ✅ Pass | Validates without error |

#### Tool Versions (from `pyproject.toml`)

| Tool | Minimum Version | Role |
|---|---|---|
| Python | ≥ 3.11 | Runtime |
| pytest | ≥ 8.3 | Test runner |
| pytest-asyncio | ≥ 0.24 | Async test support |
| pytest-cov | ≥ 6.0 | Coverage |
| ruff | ≥ 0.8 | Linting and formatting |
| mypy | ≥ 1.13 | Static type checking (strict) |
| hatchling | current | Build backend |

#### Files Verified

| File | Type | Status |
|---|---|---|
| `src/ailora/__init__.py` | Package init | ✅ |
| `src/ailora/main.py` | Entry point | ✅ |
| `src/ailora/config.py` | Pydantic-settings config | ✅ |
| `src/ailora/api/__init__.py` | API package init | ✅ |
| `src/ailora/api/app.py` | FastAPI application factory | ✅ |
| `src/ailora/api/routers/__init__.py` | Routers package init | ✅ |
| `src/ailora/api/routers/health.py` | Health probe router | ✅ |
| `Dockerfile` | Multi-stage container build | ✅ |
| `docker-compose.yml` | Local dev orchestration | ✅ |
| `.dockerignore` | Build context exclusions | ✅ |
| `pyproject.toml` | Project definition and tooling | ✅ |
| `Makefile` | Developer workflow targets | ✅ |

#### Decisions Recorded at This Gate

- README redesigned to flagship-level technical landing page with 16 required sections.
- Docker: multi-stage build (builder → runtime), non-root user (UID 1001), HEALTHCHECK,
  `postgres:16-alpine`.
- `docker-compose.yml` uses `${AILORA_DB_PASSWORD}` env-var substitution — no hardcoded secrets.
- `.dockerignore` excludes `.venv`, `.env`, `__pycache__`, `.git`, test artefacts.
- `env_file.required: false` pattern enables `docker compose config` without `.env` present.

#### Open Items Carried Forward

| ID | Item | Blocked by |
|---|---|---|
| B-01 | Prompt 06 `DOMAIN_REVIEW_REQUIRED` | Independent qualified Astrodynamics review |
| B-02 | Technical identifiers TBD in `project-identity.yaml` | Stack decisions solidify in PHASE_1 |

---

## PHASE_1 — Foundation

### Gate — 2026-08-05

**Work items closed:** P1-01 through P1-05
**Exit condition:** Build, test, and core boundaries operational.

#### Test Results

| Suite | Collected | Passed | Failed | Notes |
|---|---|---|---|---|
| `tests/test_health.py` | 2 | 2 | 0 | Liveness + readiness probes (carry-over) |
| `tests/test_readme.py` | 35 | 35 | 0 | README documentation contract (carry-over) |
| `tests/test_docker_contracts.py` | 14 | 14 | 0 | Docker contracts (carry-over) |
| `tests/test_db_baseline.py` | 19 | 19 | 0 | DB connection + Alembic baseline |
| `tests/test_domain_value_objects.py` | 33 | 33 | 0 | Domain value object contracts |
| `tests/test_observability.py` | 14 | 14 | 0 | Structured logging + tracing |
| `tests/test_ci_baseline.py` | 11 | 11 | 0 | CI workflow structural contracts |
| **Total** | **128** | **128** | **0** | Cumulative through PHASE_1 |

> Note: `test_db_baseline.py` includes 16 tests for Alembic + DB structure
> and 3 for the `aiosqlite` in-memory fixture. `test_ci_baseline.py` uses structural
> assertions on `.github/workflows/ci.yml`.

#### Quality Gate Results

| Check | Command | Result | Notes |
|---|---|---|---|
| Ruff format | `uv run ruff format --check src/ tests/` | ✅ Pass | All files formatted |
| Ruff lint | `uv run ruff check src/ tests/` | ✅ Pass | 0 issues |
| Mypy strict | `uv run mypy src/` | ✅ Pass | 0 issues in 35 source files |
| Pytest | `uv run pytest` | ✅ Pass | 128/128 passed |

#### New Files Added This Phase

| File | Type | Status |
|---|---|---|
| `src/ailora/db/__init__.py` | DB package | ✅ |
| `src/ailora/db/base.py` | SQLAlchemy declarative base | ✅ |
| `src/ailora/db/session.py` | Async session factory | ✅ |
| `src/ailora/domain/__init__.py` | Domain package | ✅ |
| `src/ailora/domain/shared/__init__.py` | Shared value objects package | ✅ |
| `src/ailora/domain/shared/value_objects.py` | Epoch, TemporalStamp, CartesianState, etc. | ✅ |
| `src/ailora/observability/__init__.py` | Observability package | ✅ |
| `src/ailora/observability/logging.py` | Structured logging (structlog + JSON) | ✅ |
| `src/ailora/observability/tracing.py` | OTel tracing (OTLP/HTTP) | ✅ |
| `.github/workflows/ci.yml` | GitHub Actions CI pipeline | ✅ |
| `alembic.ini` | Alembic configuration | ✅ |
| `alembic/env.py` | Async migration environment | ✅ |
| `alembic/versions/0001_baseline.py` | Baseline migration | ✅ |
| `tests/test_db_baseline.py` | DB baseline tests | ✅ |
| `tests/test_domain_value_objects.py` | Value object tests | ✅ |
| `tests/test_observability.py` | Observability tests | ✅ |
| `tests/test_ci_baseline.py` | CI structural tests | ✅ |

#### Decisions Recorded at This Gate

- Async SQLAlchemy 2.x with `asyncpg` (production) / `aiosqlite` (test in-memory)
- Alembic async env pattern: `run_async_migrations()` called via `asyncio.run()`
- Value objects are pure Python dataclasses — no ORM coupling
- `configure_logging()` called at app startup before first request
- CI runs on `ubuntu-latest` / Python 3.11 with `uv` for dependency management

---

## PHASE_2 — Identity and Tenancy

### Gate — 2026-08-05

**Work items closed:** P2-01 through P2-04
**Exit condition:** Authorized tenant-scoped access verified.

#### Test Results

| Suite | Collected | Passed | Failed | Notes |
|---|---|---|---|---|
| PHASE_1 carry-over | 128 | 128 | 0 | All previously passing tests |
| `tests/test_identity_models.py` | 28 | 28 | 0 | User/Tenant/Membership model contracts |
| `tests/test_auth.py` | 20 | 20 | 0 | JWT auth + password hashing |
| `tests/test_tenant_repositories.py` | 14 | 14 | 0 | Tenant-scoped repository operations |
| `tests/test_isolation.py` | 13 | 13 | 0 | Negative authz + cross-tenant isolation |
| **Total** | **203** | **203** | **0** | Cumulative through PHASE_2 |

#### Quality Gate Results

| Check | Command | Result | Notes |
|---|---|---|---|
| Ruff format | `uv run ruff format --check src/ tests/` | ✅ Pass | All files formatted |
| Ruff lint | `uv run ruff check src/ tests/` | ✅ Pass | 0 issues |
| Mypy strict | `uv run mypy src/` | ✅ Pass | 0 issues in 35 source files |
| Pytest | `uv run pytest` | ✅ Pass | 203/203 passed |

#### New Files Added This Phase

| File | Type | Status |
|---|---|---|
| `src/ailora/domain/identity/__init__.py` | Identity bounded context package | ✅ |
| `src/ailora/domain/identity/models.py` | User, Tenant, Membership, TenantRole models | ✅ |
| `src/ailora/domain/identity/repositories.py` | Tenant-scoped repository implementations | ✅ |
| `src/ailora/security/__init__.py` | Security package | ✅ |
| `src/ailora/security/auth.py` | JWT encode/decode + bcrypt password hashing | ✅ |
| `src/ailora/security/dependencies.py` | FastAPI `Depends` auth helpers | ✅ |
| `alembic/versions/0002_identity.py` | Identity migration (users, tenants, memberships) | ✅ |
| `tests/test_identity_models.py` | Identity model tests | ✅ |
| `tests/test_auth.py` | Auth tests | ✅ |
| `tests/test_tenant_repositories.py` | Repository tests | ✅ |
| `tests/test_isolation.py` | Isolation tests | ✅ |

#### Decisions Recorded at This Gate

- `bcrypt` called directly; passlib 1.7.4 does not support bcrypt ≥ 4.x
- JWT: `python-jose[cryptography]`; `sub` = user UUID string, `tenant_id`, `role`, `exp`
- Shared-database tenancy: all models carry `tenant_id` FK; repository layer enforces scoping
- `TenantAccessError` is raised (never suppressed) when membership is absent or inactive
- `test_isolation.py` verifies that cross-tenant queries return 0 rows, not errors

---

## PHASE_3 — Space Vertical Slice (Advisory)

### Gate — 2026-08-05

**Work items closed:** P3-01 through P3-07 + Oya architecture
**Exit condition:** Advisory vertical slice implemented, tested, and evidenced.
**Scientific constraint:** All conjunction/risk outputs labeled Advisory, Bounded, PHY-C1/C2.
No normative claim until Prompt 06 domain review is resolved.

#### Test Results

| Suite | Collected | Passed | Failed | Notes |
|---|---|---|---|---|
| PHASE_2 carry-over | 203 | 203 | 0 | All previously passing tests |
| `tests/test_scenario_ingestion.py` | 18 | 18 | 0 | Scenario ingestion + data classification |
| `tests/test_tle_parser.py` | 24 | 24 | 0 | TLE + state vector parser |
| `tests/test_screening.py` | 17 | 17 | 0 | Coarse conjunction screening (PHY-C1) |
| `tests/test_risk_assessment.py` | 28 | 28 | 0 | Advisory risk level + explanation |
| `tests/test_review_state.py` | 20 | 20 | 0 | Human review / approval state machine |
| `tests/test_audit.py` | 14 | 14 | 0 | Audit trail + evidence persistence |
| `tests/test_demo_scenario.py` | 21 | 21 | 0 | Reproducible demo scenario |
| `tests/test_oya.py` | 21 | 21 | 0 | Oya architecture + disabled-service contracts |
| **Total** | **366** | **366** | **0** | All tests pass, 97% line coverage |

#### Quality Gate Results

| Check | Command | Result | Notes |
|---|---|---|---|
| Ruff format | `uv run ruff format --check src/ tests/` | ✅ Pass | 55 files, all formatted |
| Ruff lint | `uv run ruff check src/ tests/` | ✅ Pass | 0 issues |
| Mypy strict | `uv run mypy src/` | ✅ Pass | 0 issues in 35 source files |
| Pytest | `uv run pytest --cov=src/ailora` | ✅ Pass | 366/366 passed, 97% coverage |

#### New Files Added This Phase

| File | Type | Status |
|---|---|---|
| `src/ailora/domain/ssa/__init__.py` | SSA bounded context package | ✅ |
| `src/ailora/domain/ssa/scenario.py` | Scenario ingestion + classification | ✅ |
| `src/ailora/domain/ssa/tle_parser.py` | TLE + state vector parser | ✅ |
| `src/ailora/domain/ssa/screening.py` | PHY-C1 coarse conjunction screening | ✅ |
| `src/ailora/domain/ssa/risk.py` | Advisory risk level + explanation | ✅ |
| `src/ailora/domain/ssa/review.py` | Human review / approval state machine | ✅ |
| `src/ailora/domain/ssa/audit.py` | Audit trail + evidence persistence | ✅ |
| `src/ailora/domain/ssa/demo.py` | Reproducible demo scenario | ✅ |
| `src/ailora/services/__init__.py` | Services package | ✅ |
| `src/ailora/services/oya/__init__.py` | Oya service package | ✅ |
| `src/ailora/services/oya/config.py` | Oya feature-flag config (disabled by default) | ✅ |
| `src/ailora/services/oya/interfaces.py` | `OyaSpeechService` ABC | ✅ |
| `src/ailora/services/oya/adapter.py` | `OyaAdapter` with 3-gate guard | ✅ |
| `tests/test_scenario_ingestion.py` | Scenario ingestion tests | ✅ |
| `tests/test_tle_parser.py` | TLE parser tests | ✅ |
| `tests/test_screening.py` | Screening tests | ✅ |
| `tests/test_risk_assessment.py` | Risk assessment tests | ✅ |
| `tests/test_review_state.py` | Review state machine tests | ✅ |
| `tests/test_audit.py` | Audit trail tests | ✅ |
| `tests/test_demo_scenario.py` | Demo scenario tests | ✅ |
| `tests/test_oya.py` | Oya architecture tests | ✅ |

#### Decisions Recorded at This Gate

- All SSA outputs carry `advisory_only=True` and `DOMAIN_REVIEW_REQUIRED` annotation
- PHY-C1 coarse screening: bounding-sphere miss-distance only; no propagation, no maneuver
- Review state machine: `PENDING → UNDER_REVIEW → APPROVED | REJECTED`; no command path
- Audit events: immutable append-only records; SHA-256 evidence hash on serialized payload
- Demo scenario: seeded, deterministic, verified expected outputs for CI regression use
- Oya Voice AI: `ENABLE_OYA_VOICE_SERVICE=false` is the safe default; `OyaAdapter.speak()`
  requires flag + API key + `PRODUCTION` environment to activate; placeholder only

#### Open Items Carried Forward

| ID | Item | Blocked by |
|---|---|---|
| B-01 | Prompt 06 `DOMAIN_REVIEW_REQUIRED` | Independent qualified Astrodynamics review |

---

## Verification Conventions

- All results in this document must correspond to actual command execution.
- A test result of PASS is only recorded after the command has been run and output inspected.
- A migration is only marked APPLIED after `alembic upgrade` has run without error.
- Timestamp references use UTC where possible.
- This file is append-only in meaning; earlier gate records must not be silently rewritten.
