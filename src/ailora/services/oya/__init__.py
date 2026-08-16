"""AILORA Oya Voice AI service package.

STATUS: Production-Grade PHASE — DISABLED / MOCKED / NON-BILLABLE.

Oya is a future Voice AI capability planned for a later stage of AILORA's
evolution.  During the production-grade phase this package provides:
  - A safe configuration model (disabled by default, fail-closed).
  - Provider-neutral interfaces and type definitions.
  - A no-op / mock adapter that never makes network calls.
  - Feature-flag gating that prevents accidental paid-service activation.

Activation is gated by:
  1. ENABLE_OYA_VOICE_SERVICE=true (explicit flag)
  2. Non-empty OYA_API_KEY (production credential)
  3. OYA_ENVIRONMENT=production (environment gate)

None of these conditions are met in production-grade/development/test environments.
"""
