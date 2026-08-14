"""AILORA space situational awareness bounded context package."""

# Register append-only audit persistence whenever any SSA submodule is imported.
from ailora.domain.ssa import audit_models as audit_models
