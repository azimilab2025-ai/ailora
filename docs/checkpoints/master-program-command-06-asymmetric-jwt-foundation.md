# Master program command 06 asymmetric JWT foundation checkpoint

Baseline: `bc0d0131ba9cbab599b4d03af34a09375cb28e36`

## Delivered

- Opt-in RS256 token issuance with exact HTTPS issuer, audience, subject, time and UUID `jti` claims.
- Algorithm and `kid` allowlisting before signature validation; generic fail-closed errors.
- Bounded key ring with one active signer, public-only retired verification keys and deterministic JWKS.
- Rotation contract that strips prior private material while preserving a limited verification overlap.
- Tests for wrong issuer/audience, algorithm confusion, unknown keys, expiry, malformed JTI and unsafe keys.

## Truth boundary

This is a local cryptographic foundation, not production key custody, OIDC, MFA, revocation storage,
provider activation, deployment or operational rotation qualification. Existing runtime authentication
is unchanged until an explicitly reviewed integration command.

## Rollback

Revert the single atomic Command 06 commit. No database migration, tenant action, credential, paid
service, provider request or Render deployment occurs in this command.
