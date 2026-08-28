# AILORA — Development Ledger

**Canonical project:** AILORA — An Azimi Innovation Lab Orbital Intelligence System
**Author / AI Architect:** Amin Azimi
**Organization:** Azimi Innovation Lab
**Authoritative source:** Prompts 01–15 (CSIP-EO-FMSP)
**Prompt 06 domain review:** PARTIAL / STILL OPEN
**Oya:** IN-REPO LIBRARY-AGENT SEPARATE / EXTERNAL GETOYA.AI LIVE IN PRODUCTION GRADE CANDIDATE FREEZE

---



#### 2026-08-28 — Companion truth alignment

- Residual-risk now splits in-repo Oya from live external getoya.ai.
- NOTICE no longer treats external Oya as an inactive future gate.
- Compose project name in .env.example is `ailora`.
- Candidate freeze identity and qualification SHA refresh remain TXT-3.

#### 2026-08-28 — External Oya live alignment

- External Oya runtime at getoya.ai verified against Render.
- Live agents: AILORA Assistant, AILORA API Agent Live.
- README contract updated; in-repo src/ailora/services/oya remains a local library-agent package.
- Historical PHASE notes below stay as dated history and are not current status.

## Timeline

| Event | Date | Status |
|---|---|---|
| Official project start | 2026-08-05 | RECORDED |
| PHASE_0 complete | 2026-08-05 | RECORDED |
| PHASE_1 complete | 2026-08-05 | RECORDED |
| PHASE_2 complete | 2026-08-05 | RECORDED |
| PHASE_3 complete | 2026-08-05 | RECORDED |
| Oya architecture documented | 2026-08-05 | RECORDED |
| Official project end | NOT_YET_COMPLETED | PENDING |

---

## Phase Log

### PHASE_0 — Repository and Engineering Baseline

**Objective:** Establish a clean, auditable project root with identity documentation,
Git history, tooling baseline, and first validated scaffold.

**Exit condition:** Build, test, and core boundaries are operational.

---

#### 2026-08-05 — PHASE_0 Day 1

| Commit | Hash | Description |
|---|---|---|
| 1 | fec0d76 | chore(repo): establish repository baseline with .gitignore |
| 2 | f088c41 | docs(identity): add approved AILORA project identity baseline |
| 3 | b3da4fb | docs(prompts): add authoritative CSIP-EO prompt sequence (Prompts 01-15) |
| 4 | 14fe77c | docs(timeline): record official project start date 2026-08-05 |

**Validations:** Documentation only — no executable code yet. No build/test/lint runs applicable.

**Decisions recorded:**
- Stack: Python / FastAPI / PostgreSQL (`PROVISIONAL_SELECTION` from Prompt 01)
- Tenancy model: `shared_database_with_tenant_key` (default from Prompt 15 §12)
- Runtime package / env prefix / DB name: TBD / NOT YET APPROVED

**Deferred (Prompt 06 blocked):**
- Any normative scientific or operational claim for conjunction risk algorithms
- PHY-C3/C4/C5 or T3/T4 propagation tiers without independent evidence

**Next unit:** Python project scaffold — `pyproject.toml`, `src/ailora/` package,
`ruff`, `mypy`, `pytest`, `Makefile` with lint/type/test targets

---

#### 2026-08-05 — PHASE_0 Gate 8

**Gate objective:** Premium README + Docker scaffold + documentation contract tests

| Commit | Hash | Description |
|---|---|---|
| 8 | a4f570f | test(readme): define flagship documentation contract |
| 9 | 6f30906 | docs(readme): establish AILORA visual foundation and hero |
| 10 | ad032da | docs(readme): add architecture capabilities and stack |
| 11 | ce94a96 | docs(readme): add setup quality safety and roadmap sections |
| 12 | 8944a74 | docs(readme): add project links hub and author profile |
| 13 | a293228 | test(docker): define Dockerfile and docker-compose contract tests |
| 14 | 96e54cc | build(docker): add Dockerfile docker-compose and .dockerignore |

**Test results:**
```
INITIAL (pre-gate):  2 collected, 2 passed (test_health.py)
FINAL (post-gate):  51 collected, 51 passed (test_health, test_readme, test_docker_contracts)

Tests added this gate:
  test_readme.py        35 tests — README documentation contract
  test_docker_contracts.py  14 tests — Dockerfile/docker-compose structural contracts
  Total new:           49 tests
```

**Quality gates:**
```
ruff format --check   ✅  11 files, all formatted
ruff check            ✅  0 issues
mypy (strict)         ✅  0 issues in 7 source files
pytest                ✅  51/51 passed
docker build          ✅  ailora:dev built successfully (multi-stage, non-root, healthcheck)
docker compose config ✅  validates without error
```

**Decisions recorded:**
- README redesigned to flagship-level technical landing page with 16 required sections
- Docker stack: multi-stage build (builder → runtime), non-root user (UID 1001), HEALTHCHECK, postgres:16-alpine
- docker-compose uses `AILORA_DB_PASSWORD` env var substitution — no hardcoded secrets
- `.dockerignore` excludes `.venv`, `.env`, `__pycache__`, `.git`, test artefacts
- `env_file.required: false` pattern enables `docker compose config` without `.env` present

**Deferred (unchanged):**
- Prompt 06 `DOMAIN_REVIEW_REQUIRED` — blocks normative scientific claims

**PHASE_0 status: ✅ COMPLETE — all P0-01 through P0-08 items done.**

---

### PHASE_1 — Foundation

**Objective:** FastAPI app skeleton, database connection, domain value objects,
observability bootstrap, and CI/CD baseline.

**Exit condition:** Build, test, and core boundaries are operational.

| Commit | Hash | Description |
|---|---|---|
| P1-01 | (pre-existing) | FastAPI app skeleton — validated |
| P1-02 | 66de8b7 | feat(db): add database connection + Alembic migration baseline |
| P1-03 | bedaf69 | feat(domain): add core domain value objects |
| P1-04 | e597278 | feat(observability): add structured logging and OTel tracing bootstrap |
| P1-05 | 6648dec | feat(ci): add GitHub Actions CI baseline |

**Test results:**
```
INITIAL (entering phase):  51 collected, 51 passed
FINAL (post-phase):       144 collected, 144 passed

Tests added this phase:
  test_db_baseline.py              19 tests — DB + Alembic baseline
  test_domain_value_objects.py     33 tests — domain value object contracts
  test_observability.py            14 tests — structured logging + tracing
  test_ci_baseline.py              11 tests — CI workflow structural contracts
  Total new:                       77 tests
```

**Quality gates:**
```
ruff format --check   ✅  pass
ruff check            ✅  0 issues
mypy (strict)         ✅  0 issues in 35 source files
pytest                ✅  144/144 passed
```

**Decisions recorded:**
- DB: async SQLAlchemy 2.x with `asyncpg`; `aiosqlite` for in-memory test fixtures
- Alembic: async env (`run_async_migrations`); migration 0001 establishes baseline schema
- Value objects: `Epoch`, `TemporalStamp`, `CartesianState`, `OrbitalRegime`, `ReferenceFrame`, `EpochScale`
- Observability: `configure_logging()` (structlog + JSON) + `configure_tracing()` (OTel + OTLP/HTTP)
- CI: GitHub Actions — ruff format, ruff check, mypy, pytest (Ubuntu, Python 3.11)

**PHASE_1 status: ✅ COMPLETE — all P1-01 through P1-05 items done.**

---

### PHASE_2 — Identity and Tenancy

**Objective:** User/Tenant/Membership/Role models, JWT auth middleware,
tenant-scoped DB access, and negative authorization tests.

**Exit condition:** Authorized tenant-scoped access verified.

| Commit | Hash | Description |
|---|---|---|
| P2-01 | 08d6d09 | feat(identity): add User/Tenant/Membership domain models + migration |
| P2-02 | bcb28a5 | feat(auth): add JWT auth middleware and password hashing |
| P2-03 | 7bcf815 | feat(repositories): add tenant-scoped DB access layer |
| P2-04 | 9fd69b5 | test(isolation): add negative authorization + cross-tenant isolation tests |

**Test results:**
```
INITIAL (entering phase):  144 collected, 144 passed
FINAL (post-phase):        219 collected, 219 passed

Tests added this phase:
  test_identity_models.py          28 tests — User/Tenant/Membership model contracts
  test_auth.py                     20 tests — JWT auth + password hashing
  test_tenant_repositories.py      14 tests — tenant-scoped repository operations
  test_isolation.py                13 tests — negative authz + cross-tenant isolation
  Total new:                       75 tests
```

**Quality gates:**
```
ruff format --check   ✅  pass
ruff check            ✅  0 issues
mypy (strict)         ✅  0 issues in 35 source files
pytest                ✅  219/219 passed
```

**Decisions recorded:**
- bcrypt called directly (not via passlib) due to bcrypt 5.x / passlib 1.7.4 incompatibility
- JWT: `python-jose[cryptography]`; claims include `sub` (user_id), `tenant_id`, `role`, `exp`
- Tenancy model: `shared_database_with_tenant_key` (per Prompt 15 §12)
- Migration 0002: `users`, `tenants`, `memberships` tables with FK + unique constraints
- `TenantAccessError` raised on missing/inactive membership — never leaks cross-tenant data

**PHASE_2 status: ✅ COMPLETE — all P2-01 through P2-04 items done.**

---

### PHASE_3 — Space Vertical Slice (Advisory)

**Objective:** Scenario ingestion, TLE parsing, coarse conjunction screening,
advisory risk output, human review state machine, audit trail, and demo scenario.

**Exit condition:** Slice implemented, tested, and evidenced.
**Scientific constraint:** All outputs labeled Advisory, Bounded, PHY-C1/C2. No normative
claim until Prompt 06 domain review is resolved.

| Commit | Hash | Description |
|---|---|---|
| P3-01 | a8382f5 | feat(ssa): add scenario ingestion + data classification |
| P3-02 | 0c2f67b | feat(ssa): add synthetic TLE/state vector parser |
| P3-03 | abf5b68 | feat(ssa): add T0/PHY-C1 coarse conjunction screening |
| P3-04 | bf2c448 | feat(ssa): add advisory risk level and explanation output |
| P3-05 | f8d4c77 | feat(ssa): add human review/approval state machine |
| P3-06 | 555629f | feat(ssa): add audit trail and evidence persistence |
| P3-07 | 22d708c | feat(ssa): add reproducible demo scenario — PHASE_3 complete |
| Oya   | a9d38d2 | feat(oya): add Oya Voice AI architecture docs, disabled config, and placeholder module |
| fmt   | 51a0d47 | style: apply ruff format to all source and test files |

**Test results:**
```
INITIAL (entering phase):  219 collected, 219 passed
FINAL (post-phase):        366 collected, 366 passed

Tests added this phase:
  test_scenario_ingestion.py       18 tests — scenario ingestion + data classification
  test_tle_parser.py               24 tests — TLE/state vector parser
  test_screening.py                17 tests — coarse conjunction screening
  test_risk_assessment.py          28 tests — advisory risk level + explanation
  test_review_state.py             20 tests — human review/approval state machine
  test_audit.py                    14 tests — audit trail + evidence persistence
  test_demo_scenario.py            21 tests — reproducible demo scenario
  test_oya.py                      21 tests — Oya architecture contracts
  Total new:                       163 tests
```

**Quality gates:**
```
ruff format --check   ✅  pass (55 files, all formatted)
ruff check            ✅  0 issues
mypy (strict)         ✅  0 issues in 35 source files
pytest                ✅  366/366 passed (97% coverage)
```

**Decisions recorded:**
- All SSA outputs annotated with `DOMAIN_REVIEW_REQUIRED` / `advisory_only=True`
- PHY-C1 coarse screening only (no propagation, no maneuver recommendation)
- Human review state machine: PENDING → UNDER_REVIEW → APPROVED/REJECTED (no command path)
- Audit trail: immutable append-only `AuditEvent` records with actor, timestamp, and evidence hash
- Demo scenario: deterministic, seeded, produces expected risk + review outputs for CI regression
- Oya Voice AI: architecture documented in README; service disabled (`ENABLE_OYA_VOICE_SERVICE=false`);
  placeholder module at `src/ailora/services/oya/`; 3-gate activation guard in `OyaAdapter.speak()`

**PHASE_3 status: ✅ COMPLETE — all P3-01 through P3-07 items done. Oya architecture documented.**

---

## Open Work Items (ordered, smallest-first)

### PHASE_0 — Engineering Baseline

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P0-01 | `.gitignore` + repo baseline | ✅ DONE | — |
| P0-02 | Identity docs | ✅ DONE | — |
| P0-03 | Prompt sequence docs | ✅ DONE | — |
| P0-04 | Timeline + CHANGELOG | ✅ DONE | — |
| P0-05 | DEVLOG | ✅ DONE | — |
| P0-06 | Python scaffold (`pyproject.toml`, `src/ailora/`, tooling) | ✅ DONE | — |
| P0-07 | Dockerfile + docker-compose skeleton | ✅ DONE | — |
| P0-08 | `docs/verification.md` skeleton | ✅ DONE | — |

### PHASE_1 — Foundation

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P1-01 | FastAPI app skeleton with health endpoint | ✅ DONE | — |
| P1-02 | Database connection + migration baseline (Alembic) | ✅ DONE | — |
| P1-03 | Core domain value objects (TemporalStamp, Epoch, Frame) | ✅ DONE | — |
| P1-04 | Observability bootstrap (OpenTelemetry, structured logging) | ✅ DONE | — |
| P1-05 | CI/CD baseline (GitHub Actions) | ✅ DONE | — |

### PHASE_2 — Identity and Tenancy

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P2-01 | User / Tenant / Membership / Role domain models | ✅ DONE | — |
| P2-02 | JWT auth middleware | ✅ DONE | — |
| P2-03 | Tenant-scoped DB access layer | ✅ DONE | — |
| P2-04 | Negative authorization + cross-tenant isolation tests | ✅ DONE | — |

### PHASE_3 — Space Vertical Slice (Advisory / T0-T1 / PHY-C1-C2)

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P3-01 | Scenario ingestion with data classification | ✅ DONE | — |
| P3-02 | Synthetic TLE/state vector parsing | ✅ DONE | — |
| P3-03 | Coarse conjunction screening (T0, PHY-C1, Advisory) | ✅ DONE | — |
| P3-04 | Risk level + explanation output (Advisory-only) | ✅ DONE | — |
| P3-05 | Human review / approval state (no command path) | ✅ DONE | — |
| P3-06 | Audit trail + evidence persistence | ✅ DONE | — |
| P3-07 | Reproducible demo scenario + expected outputs | ✅ DONE | — |

**PHASE_3 scientific note:** All conjunction/risk outputs labeled Advisory, Bounded, PHY-C1/C2.
No normative claim until Prompt 06 domain review is resolved.

---

## Blockers

| ID | Description | Resolution path |
|---|---|---|
| B-01 | Prompt 06 `DOMAIN_REVIEW_REQUIRED` | Independent qualified Astrodynamics review required |
| B-02 | TBD technical identifiers (runtime_package, db_name, env_prefix, etc.) | Will resolve as stack decisions solidify during PHASE_0/1 |

---

## Prohibited Actions (permanent reminder)

- Spacecraft Command / Telecommand / Uplink: PERMANENTLY_DENIED
- Oya implementation: NOT_AUTHORIZED in this phase
- Production deploy / public release: NOT_AUTHORIZED
- Push / remote / PR: NOT_AUTHORIZED (local commits only)

---

### 2026-08-20 — Local evidence surfaces (Commands 20-30)

- Minimal frozen evidence types added for ENT-015 through ENT-023 local scope.
- Test count baseline synchronized to 1065 collected tests.
- Governance remaining_scope annotated; EXTERNAL_GATE and PARTIAL statuses intentionally unchanged.
- Oya remains library-agent / DISABLED by design.
- Prompt 06 domain review remains PARTIAL / STILL OPEN.

