# Command 17 internal SLO and synthetic contracts

This bounded repository change adds deterministic workflow availability, latency,
error-budget, burn-rate, scientific-outcome and synthetic-freshness contracts.
Dimensions are allowlisted and bounded; tenant identifiers and secrets are rejected.
Synthetic results are advisory-only and cannot create operational authority.

This is internal design and executable-test evidence only. It does not provide or
claim an external OpenTelemetry backend, dashboard, alert delivery, production
synthetic runner, measured workload, durable production broker, or operational
qualification. `ENT-010` remains `PARTIAL`, and its external dependency remains open.
