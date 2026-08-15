# Independent Astrodynamics Verification Evidence

## Status and authority

- Capability: `C-12`.
- Status: bounded differential software evidence; independent scientific approval remains an
  external gate.
- No repository test, fixture, comparison, or author may self-issue qualified scientific,
  normative, operational, collision-probability, maneuver, or command authority.

## Implemented contract

- Immutable independent-reference inputs with engine identity, version, source revision,
  source digest, content digest, declared primary algorithm, frame, epoch, time scale, and units.
- Deterministic absolute-plus-relative tolerance comparison for TCA epoch, miss distance,
  relative position, and relative velocity.
- Explicit agreement, material-disagreement, and reference-unavailable states.
- Same-engine reuse is rejected as non-independent.
- Missing or discrepant evidence never becomes agreement or pass.

## Deliberate limitations

- No second scientific engine is installed or activated by this command.
- A reference is accepted only as supplied evidence; scientific competence, methodology,
  independence, and approval require qualified external review.
- Frame transformation, covariance propagation, encounter-plane projection, HBR, and collision
  probability remain deferred.
- No network, database, API, provider, deployment, maneuver, or command path is introduced.

## Verification evidence

- Boundary-equality, deterministic replay, missing-reference, material-disagreement,
  same-engine, false-attestation, semantic-mismatch, and digest-tampering tests.
- Full Ruff, strict Mypy, full pytest, and package-content gates are required before commit.
