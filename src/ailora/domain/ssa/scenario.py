"""
AILORA Scenario Ingestion and Data Classification.

A Scenario is the primary ingestion unit for a conjunction risk assessment.
Each scenario is:
  - Tenant-scoped (tenant_id mandatory)
  - Advisory-only (no operational commands ever)
  - Data-classified (see DataClassification)
  - Bounded to the EARTH_ORBIT_ONLY active regimes per project-identity.yaml

Prompt 06 boundary reminder:
  All outputs are Advisory, Bounded, and labeled PHY-C1/C2 (non-normative)
  until the Prompt 06 Astrodynamics domain review is complete.

No spacecraft command, telecommand, uplink, or autonomous maneuver execution
path exists in this module — permanently denied.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

from pydantic import BaseModel, Field

from ailora.domain.shared.value_objects import (
    Epoch,
    OrbitalRegime,
    ReferenceFrame,
    TemporalStamp,
)

# ---------------------------------------------------------------------------
# Data classification
# ---------------------------------------------------------------------------


class DataClassification(StrEnum):
    """
    Data sensitivity classification for scenario inputs and outputs.

    SYNTHETIC   — Generated or simulated data; safe for development and testing.
    UNCLASSIFIED — Real public data (e.g. NORAD public catalog).
    RESTRICTED  — Non-public data requiring access control; not for demo scenarios.
    """

    SYNTHETIC = "SYNTHETIC"
    UNCLASSIFIED = "UNCLASSIFIED"
    RESTRICTED = "RESTRICTED"


class DataProvenance(BaseModel):
    """Provenance record for a data input."""

    model_config = {"frozen": True}

    source_label: str = Field(
        ...,
        max_length=256,
        description="Human-readable label for the data source",
    )
    classification: DataClassification = Field(
        default=DataClassification.SYNTHETIC,
        description="Sensitivity classification",
    )
    ingested_at: Epoch = Field(
        ...,
        description="Epoch at which the data was ingested",
    )
    is_synthetic: bool = Field(
        default=True,
        description="True if the data is purely synthetic (no real-world objects)",
    )


# ---------------------------------------------------------------------------
# Orbital object descriptor
# ---------------------------------------------------------------------------


class OrbitalObjectDescriptor(BaseModel):
    """
    Minimal descriptor for an orbital object in a scenario.

    Carries only the information needed for T0/PHY-C1 screening.
    A real scenario would replace the synthetic values with parsed TLE data.
    """

    model_config = {"frozen": True}

    object_id: str = Field(
        ...,
        max_length=64,
        description="Platform-internal identifier (e.g. NORAD ID or synthetic label)",
    )
    object_name: str = Field(
        default="",
        max_length=128,
        description="Human-readable name for display purposes",
    )
    regime: OrbitalRegime = Field(
        default=OrbitalRegime.UNKNOWN,
        description="Best-known orbital regime",
    )
    provenance: DataProvenance


# ---------------------------------------------------------------------------
# ConjunctionScenario — primary ingestion unit
# ---------------------------------------------------------------------------


class ConjunctionScenario(BaseModel):
    """
    A conjunction risk assessment scenario.

    Contains two orbital objects (primary and secondary) at a common epoch,
    classified by data source, and scoped to a tenant.

    Advisory-only: No output from this scenario constitutes an operational
    recommendation or command.  All outputs are bounded and non-normative
    until Prompt 06 domain review is complete.
    """

    model_config = {"frozen": True}

    scenario_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Platform-unique scenario identifier",
    )
    tenant_id: uuid.UUID = Field(
        ...,
        description="Owning tenant — must be verified against authenticated identity",
    )
    reference_epoch: TemporalStamp = Field(
        ...,
        description="Temporal context for this scenario (epoch + frame)",
    )
    primary_object: OrbitalObjectDescriptor = Field(
        ...,
        description="Primary (protected) orbital object",
    )
    secondary_object: OrbitalObjectDescriptor = Field(
        ...,
        description="Secondary (threatening) orbital object",
    )
    ingestion_notes: str = Field(
        default="",
        max_length=1024,
        description="Optional human notes about ingestion conditions",
    )

    # Advisory-only sentinel — permanently non-operational
    ADVISORY_ONLY: bool = Field(
        default=True,
        frozen=True,
        description="Permanently True: all outputs are advisory-only",
    )

    @property
    def combined_classification(self) -> DataClassification:
        """
        Return the more restrictive data classification of the two objects.

        RESTRICTED > UNCLASSIFIED > SYNTHETIC
        """
        rank = {
            DataClassification.SYNTHETIC: 0,
            DataClassification.UNCLASSIFIED: 1,
            DataClassification.RESTRICTED: 2,
        }
        p_cls = self.primary_object.provenance.classification
        s_cls = self.secondary_object.provenance.classification
        return p_cls if rank[p_cls] >= rank[s_cls] else s_cls

    @property
    def frame(self) -> ReferenceFrame:
        """Return the reference frame from the scenario epoch."""
        return self.reference_epoch.frame
