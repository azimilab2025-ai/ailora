# Master Program Command 19 — time, EOP, leap-second and ITRF checkpoint

## Decision

`INTERNAL_TIME_EOP_LEAP_ITRF_BASELINE_VERIFIED_EXTERNAL_SCIENTIFIC_GATE_OPEN`

## Evidence

- First-class UTC, TAI, TT and UT1 typed values are deterministic and digest-bound.
- Pinned offline EOP and leap-second datasets carry explicit identity, range and lineage.
- TEME-to-ITRF position/velocity conversion uses pinned Astropy ITRS with bounded failures.
- Focused tests preserve leap-second insertion, EOP status, ITRF regression and round-trip
  behavior while rejecting independent-truth overclaims.
- Full repository tests, coverage, formatting, lint and type checks are required by the
  implementing command before its atomic local commit.

## Truthful boundary

ENT-012 remains `PARTIAL`. The local numeric fixture shares the Astropy/PyERFA implementation
lineage and is not independent truth. Independent vectors, scientific review and
release-specific tolerance acceptance remain external. No network activation, paid action,
deployment, production release, physical authority or spacecraft-command capability is added.
