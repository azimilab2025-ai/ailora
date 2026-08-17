# AILORA Command 14 — Scientific Reproducibility Manifest

Baseline: `8b3cfd22ba88e65a56b28e95878650878f21469d`

## Status

`CONTENT_ADDRESSED_SCIENTIFIC_MANIFEST_AND_FAIL_CLOSED_DRIFT_BASELINE_VERIFIED`

This command implements deterministic local evidence for scientific configuration and execution.
It does not call a provider, activate a runtime route, execute a database migration, invoke Render,
approve scientific operation or create any spacecraft command capability.

## Implemented reproducibility boundary

- Five mandatory registry namespaces bind algorithms, datasets, configurations, runtimes and
  tolerance profiles to immutable versions and lowercase SHA-256 content digests.
- Mutable version labels such as `latest`, `HEAD`, `main`, `master` and `unversioned` fail closed.
- The execution context binds a full Git commit, supported Python runtime, platform identifier,
  explicit random seed and timezone-aware UTC observation time.
- The declared Python 3.11/3.12 runtime matrix and canonical registry/tolerance ordering are
  included in the digest-bound payload.
- Tolerances require explicit units, unique names, finite nonnegative values, at least one positive
  bound and the immutable `FAIL_CLOSED` drift policy.
- A scientific fingerprint covers every execution-relevant input while excluding only execution
  identity and observation time. Comparisons reject source, runtime, platform, seed, registry,
  matrix or tolerance drift.
- Envelope, payload, fingerprint, schema, status and production-authority tampering are rejected.
  Evidence remains advisory-only and cannot authorize production or scientific operation.

## Verification

Forty-three focused tests cover deterministic serialization, canonical ordering, all five registry
namespaces, version and digest constraints, tolerance validity, runtime/source/seed drift, registry
and tolerance drift, timezone and authority boundaries, malformed documents and nested digest
tampering. The complete repository suite passes with 941 tests and 88.72% statement coverage.

## Remaining qualification gates

- Bind manifest generation to each applicable scientific execution and persistence path.
- Retain promoted manifests in immutable release evidence and define custody and approval roles.
- Run controlled cross-platform repeatability exercises with pinned dependency and dataset bytes.
- Obtain independent scientific configuration review and release-specific tolerance acceptance.
- Keep proximity severity distinct from collision probability and preserve advisory-only authority.

ENT-011 is `VERIFIED_BASELINE` for the declared local content-addressed manifest and drift scope.
Independent review, runtime adoption and operational scientific acceptance remain open and cannot be
inferred from this checkpoint.
