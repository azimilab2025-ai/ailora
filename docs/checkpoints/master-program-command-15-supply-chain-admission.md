# AILORA Command 15 — Supply-Chain Evidence Admission

Baseline: `f37ea1fbcfdf81cc9954bba3c6b972615b46ace9`

## Status

`CONTENT_ADDRESSED_SIGNED_SUPPLY_CHAIN_ADMISSION_BASELINE_VERIFIED`

This command strengthens local, provider-neutral supply-chain evidence. It does not invoke an
external scanner; provision, persist or expose a protected release private key; sign a release with
a protected identity; publish an artifact; mutate a registry; activate deployment admission; call
Render; or authorize production. Tests use only ephemeral in-memory signing keys.

## Implemented admission boundary

- The CycloneDX 1.6 generator inventories every registry package and version resolved in `uv.lock`,
  including all available locked distribution SHA-256 hashes; direct-dependency-only inventory is
  no longer represented as a complete SBOM.
- Artifact references must be immutable `name@sha256:digest` values. Mutable tags and abbreviated,
  uppercase or malformed digests fail closed.
- SAST, SCA, container and secret-history evidence must each appear exactly once, name an immutable
  scanner version, bind to the promoted artifact digest, report zero findings and pass.
- VEX statements bind vulnerability, component PURL, justification and statement digest. Known
  affected and under-investigation states deny admission; absence is never treated as not affected.
- The manifest binds the full source commit, trusted builder, SLSA provenance predicate, SBOM, VEX,
  scan results, source and target environments, bounded UTC validity and a no-rebuild invariant.
- Ed25519 verification accepts only injected trusted public keys. The repository contains no
  signing private key and the verifier performs no key discovery or network access.
- Canonical serialization, outer digest and signature all cover the complete manifest. Added,
  removed, malformed, reordered or recomputed authority-boundary fields fail closed.
- A successful result is explicitly `EVIDENCE_VERIFIED_NOT_DEPLOYMENT_AUTHORIZATION`; even a
  production target remains unapproved and requires separate human and platform enforcement.

## Verification

Forty-three focused tests cover immutable artifact references, Git and evidence digests, all scan
classes, artifact binding, failure and incompleteness, VEX states, bounded UTC validity, trusted
builders and public keys, Ed25519 signature failure, exact payload shape, canonical order, boundary
tampering, no-rebuild and permanent no-deployment-authority semantics. SBOM tests compare the
complete generated component set to the lock and verify deterministic hashes and secret exclusion.
The complete repository suite passes with 984 tests and 88.77% statement coverage.

## Remaining qualification gates

- Run approved SAST, SCA, container and full-history secret scanners in governed CI against the
  exact built artifact and retain their native reports immutably.
- Provision protected signing identity and custody, revocation, rotation and incident procedures.
- Publish artifact, CycloneDX SBOM, OpenVEX and SLSA provenance as immutable registry referrers.
- Enforce signature, builder, digest and evidence policy at the selected deployment admission point.
- Obtain independent supply-chain review and accept release-specific residual risk.

ENT-008 is `VERIFIED_BASELINE` only for complete-lock inventory and local signed-admission
semantics. Scanner results, protected signing, immutable publication and operational enforcement
remain open external gates; no release or deployment approval is inferred.
