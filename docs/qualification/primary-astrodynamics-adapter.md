# Primary Astrodynamics Adapter Qualification

Status: **IMPLEMENTED AND TESTED - INDEPENDENT SCIENTIFIC APPROVAL PENDING**

- Algorithm: SGP4/SDP4 through `sgp4` 2.27
- Package source: https://pypi.org/project/sgp4/2.27/
- Upstream source: https://github.com/brandon-rhodes/python-sgp4
- Golden TLE source: https://github.com/brandon-rhodes/python-sgp4/blob/master/sgp4/SGP4-VER.TLE
- Golden vector source: https://github.com/brandon-rhodes/python-sgp4/blob/master/sgp4/tcppver.out
- Golden case identity: satellite 00005, `tsince=0.00000000`
- Declared license: MIT
- Installed license-file SHA-256: `4474ea9eccbb829c6bc3652381bfe78b1c815de021d4a284a2a5b383a374d030`
- Gravity constants: WGS-72
- Native output: TEME, kilometres, kilometres per second
- Default validity window: plus or minus 14 days from the TLE epoch

The implementation is deterministic and verified against the public Vallado SGP4
verification case for satellite 00005. It does not convert TEME to GCRF, ITRF, or
ECEF and does not claim independent scientific approval. That approval remains an
external C-12 gate. TLE accuracy limitations remain distinct from implementation
agreement with a reference vector.

No provider access, operational command, maneuver recommendation, collision
probability, production write, deployment, credential, paid, or Oya action occurred.
