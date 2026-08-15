# DevSecOps and supply-chain qualification

CI uses explicit read-only permissions, job timeouts, immutable third-party Action commit SHAs, locked dependencies, Ruff security rules, strict Mypy, a measured 85 percent coverage floor, full tests, local SBOM generation, and wheel/sdist builds. The SBOM is a deterministic direct-dependency inventory. Independent vulnerability assessment, penetration testing, production attestation, and signing authority remain external gates. No production signing key is created or used.
