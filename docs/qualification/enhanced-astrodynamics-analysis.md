# Enhanced Astrodynamics Analysis Qualification Evidence

## Status and authority

- Capability: `C-11`.
- Status: advisory-only software evidence; independent scientific approval is deferred to C-12.
- This implementation does not issue a normative, qualified, operationally authoritative,
  maneuver, command, or collision-probability result.

## Implemented bounded scope

- Deterministic closest-approach search over an explicit UTC interval.
- Native TEME relative state in km and km/s using the pinned C-10 SGP4 2.27 boundary.
- Explicit evaluation, iteration, time-tolerance, distance-tolerance, and validity bounds.
- Six-by-six Cartesian TEME covariance validation with explicit epoch, component ordering,
  units, one-sigma meaning, source revision, digest, correlation scope, finiteness,
  symmetry, and positive-semidefinite checks.
- Conservative uncertainty radius computed as `k * sqrt(trace(C_rel_position))` only when
  primary/secondary covariance epochs align with TCA and independence is explicitly assumed.
- Safe labels preserve missing uncertainty and numerical limitations as review-required.

## Explicit limitations

- The TCA is a bounded-search estimate, not proof of a global optimum outside the interval.
- Numerical time precision is recorded; physical TCA time uncertainty is unavailable.
- Covariance propagation, covariance frame transformation, EOP/leap-second-backed frame
  transformation, encounter-plane projection, HBR, and collision probability are not implemented.
- Cross-object covariance correlation is unavailable; combination requires an explicit
  independence assumption and records that limitation.
- Covariance condition number is not computed. Uses requiring inversion or condition-dependent
  inference remain blocked.
- No API, database, provider, network, production, deployment, maneuver, or command path exists.

## Verification evidence

- Analytic synthetic crossing, endpoint, deterministic fixed-SGP4 regression, invalid-window,
  evaluation-budget, and non-convergence tests.
- Covariance shape, finite-value, symmetry, PSD, epoch-alignment, correlation-assumption,
  conservative-bound, and threshold-boundary tests.
- Full Ruff, strict Mypy, existing pytest, and package-content gates are required before commit.

## Reference context

- NASA Conjunction Assessment Risk Analysis: <https://www.nasa.gov/cara/>
- NASA CARA Tools, NTRS 20240005634: <https://ntrs.nasa.gov/citations/20240005634>
- NASA conjunction assessment operations report, NTRS 20100015203:
  <https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20100015203.pdf>

These references provide traceable external context. They do not constitute approval of this
implementation, its thresholds, or its scientific fitness.
