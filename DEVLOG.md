# AILORA — Development Ledger

**Canonical project:** AILORA — An Azimi Innovation Lab Orbital Intelligence System
**Author / AI Architect:** Amin Azimi
**Organization:** Azimi Innovation Lab
**Authoritative source:** Prompts 01–15 (CSIP-EO-FMSP)
**Prompt 06 domain review:** PARTIAL / STILL OPEN
**Oya:** PLANNED / NOT CURRENTLY IMPLEMENTED

---

## Timeline

| Event | Date | Status |
|---|---|---|
| Official project start | 2026-08-05 | RECORDED |
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

## Open Work Items (ordered, smallest-first)

### PHASE_0 — Engineering Baseline

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P0-01 | `.gitignore` + repo baseline | ✅ DONE | — |
| P0-02 | Identity docs | ✅ DONE | — |
| P0-03 | Prompt sequence docs | ✅ DONE | — |
| P0-04 | Timeline + CHANGELOG | ✅ DONE | — |
| P0-05 | DEVLOG | 🔄 IN PROGRESS | — |
| P0-06 | Python scaffold (`pyproject.toml`, `src/ailora/`, tooling) | ⬜ TODO | — |
| P0-07 | Dockerfile + docker-compose skeleton | ⬜ TODO | — |
| P0-08 | `docs/verification.md` skeleton | ⬜ TODO | — |

### PHASE_1 — Foundation

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P1-01 | FastAPI app skeleton with health endpoint | ⬜ TODO | P0-06 |
| P1-02 | Database connection + migration baseline (Alembic) | ⬜ TODO | P1-01 |
| P1-03 | Core domain value objects (TemporalStamp, Epoch, Frame) | ⬜ TODO | P1-01 |
| P1-04 | Observability bootstrap (OpenTelemetry, structured logging) | ⬜ TODO | P1-01 |
| P1-05 | CI/CD baseline (GitHub Actions) | ⬜ TODO | P0-06 |

### PHASE_2 — Identity and Tenancy

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P2-01 | User / Tenant / Membership / Role domain models | ⬜ TODO | P1-02 |
| P2-02 | JWT auth middleware | ⬜ TODO | P2-01 |
| P2-03 | Tenant-scoped DB access layer | ⬜ TODO | P2-01 |
| P2-04 | Negative authorization + cross-tenant isolation tests | ⬜ TODO | P2-03 |

### PHASE_3 — Space Vertical Slice (Advisory / T0-T1 / PHY-C1-C2)

| ID | Item | Status | Blocked by |
|---|---|---|---|
| P3-01 | Scenario ingestion with data classification | ⬜ TODO | P2-03 |
| P3-02 | Synthetic TLE/state vector parsing | ⬜ TODO | P3-01 |
| P3-03 | Coarse conjunction screening (T0, PHY-C1, Advisory) | ⬜ TODO | P3-02 |
| P3-04 | Risk level + explanation output (Advisory-only) | ⬜ TODO | P3-03 |
| P3-05 | Human review / approval state (no command path) | ⬜ TODO | P3-04 |
| P3-06 | Audit trail + evidence persistence | ⬜ TODO | P3-05 |
| P3-07 | Reproducible demo scenario + expected outputs | ⬜ TODO | P3-06 |

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
