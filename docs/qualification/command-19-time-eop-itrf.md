# Command 19 — internal time, EOP, leap-second and ITRF qualification

## Implemented local baseline

- UTC, TAI, TT and UT1 are explicit typed representations of one canonical instant.
- The pinned offline `finals2000A.all` EOP file is bound by version, SHA-256, MJD range,
  UT1 status, polar-motion status and a lineage digest.
- The embedded PyERFA leap-second table is bound by version, complete canonical digest,
  first/last records, record count and the epoch-specific TAI-UTC offset.
- TEME position and velocity are transformed together to an ITRF candidate realized as
  pinned Astropy ITRS, with explicit units, epoch, frame labels and transformation digest.
- Missing, out-of-range, degraded, non-finite or ambiguous inputs fail closed.
- Runtime download and network paths remain disabled.

## Probe-bound regression evidence

The Vallado input state at `2000-06-27T18:50:19.733568Z` produces the pinned local
Astropy/PyERFA ITRF regression result recorded by the focused tests. Round-trip checks,
timezone canonicalization, leap-boundary semantics and deterministic digests are exercised.

This numeric fixture is explicitly `PINNED_SAME_ENGINE_REGRESSION`. Astropy time/frame
operations and PyERFA share a common implementation lineage; therefore this evidence is not
an independent truth vector, differential engine, IV&V result or final scientific approval.

## Open external gate

ENT-012 remains `PARTIAL`. Independently sourced truth vectors, independent scientific
review and release-specific tolerance acceptance remain required under
`G04_SCIENTIFIC_QUALIFICATION`. No operational, spacecraft-command, production-release or
deployment authority is created by this local baseline.
