"""Typed, versioned, advisory-only space-data semantic boundary."""

from ailora.domain.space_data.contracts import ObservationEnvelope, Provenance
from ailora.domain.space_data.service import IngestionResult, IngestionStatus

__all__ = ["IngestionResult", "IngestionStatus", "ObservationEnvelope", "Provenance"]
