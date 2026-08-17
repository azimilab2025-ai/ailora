"""Fail-closed bridge from qualified provider TLE bytes to native TEME observations.

This module does not perform or claim TEME-to-GCRF conversion. A qualified GCRF
path requires governed IERS Earth-orientation inputs and independent scientific review.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.space_data.contracts import (
    DataQuality,
    DistanceUnit,
    ReferenceFrame,
    SchemaVersion,
    SpaceDataClassification,
    TimeScale,
    VelocityUnit,
    canonical_payload_digest,
)
from ailora.domain.space_data.service import IngestionResult, SpaceDataIngestionService
from ailora.domain.ssa.tle_parser import parse_tle
from ailora.services.astrodynamics.adapter import Sgp4Engine
from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.interfaces import AstrodynamicsError
from ailora.services.astrodynamics.models import PropagationRequest, TLEInput
from ailora.services.astrodynamics.service import AstrodynamicsService
from ailora.services.space_data.interfaces import ProviderResponse


def _same_catalog(left: str, right: str) -> bool:
    return (left.lstrip("0") or "0") == (right.lstrip("0") or "0")


def _tle_lines(response: ProviderResponse) -> tuple[str, str, str]:
    if not response.content_type.lower().startswith("text/plain"):
        raise ValueError("provider TLE content type is invalid")
    text = response.payload.decode("utf-8", errors="strict")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 3:
        raise ValueError("provider TLE payload must contain exactly three nonblank lines")
    record = parse_tle(lines[0], lines[1], lines[2])
    if not _same_catalog(record.catalog_number, response.object_id):
        raise ValueError("provider object identity does not match TLE catalog identity")
    return lines[0], lines[1], lines[2]


class TLEObservationBridge:
    """Transform bounded provider TLE bytes into tenant-scoped native TEME evidence."""

    def __init__(
        self,
        database: AsyncSession,
        *,
        propagation: AstrodynamicsService | None = None,
        ingestion: SpaceDataIngestionService | None = None,
    ) -> None:
        self._propagation = propagation or AstrodynamicsService(AstrodynamicsConfig(), Sgp4Engine())
        self._ingestion = ingestion or SpaceDataIngestionService(database)

    async def ingest(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        response: ProviderResponse,
        evaluated_at: datetime,
        classification: SpaceDataClassification,
        max_age_seconds: float = 0.0,
    ) -> IngestionResult:
        raw_digest = hashlib.sha256(response.payload).hexdigest()
        try:
            name, line1, line2 = _tle_lines(response)
            propagation = self._propagation.propagate(
                PropagationRequest(
                    request_id=response.request_id,
                    tle=TLEInput(name, line1, line2),
                    target_epoch=evaluated_at,
                    purpose="advisory provider TLE normalization",
                )
            )
            source_version = (
                f"{response.provider_version}|{propagation.algorithm_id}-"
                f"{propagation.algorithm_version}|RAW-{raw_digest}"
            )
            provenance: dict[str, object] = {
                "source_id": response.provider_id,
                "source_version": source_version,
                "ingested_at": response.fetched_at,
                "canonical_digest": "0" * 64,
                "classification": SpaceDataClassification(classification),
            }
            payload: dict[str, object] = {
                "tenant_id": tenant_id,
                "observation_id": f"{response.provider_id}:{response.request_id.hex}",
                "object_id": response.object_id,
                "schema_version": SchemaVersion.V1,
                "reference_frame": ReferenceFrame(propagation.frame.value),
                "distance_unit": DistanceUnit(propagation.distance_unit.value),
                "velocity_unit": VelocityUnit(propagation.velocity_unit.value),
                "time_scale": TimeScale.UTC,
                "epoch": propagation.target_epoch,
                "evaluated_at": propagation.target_epoch,
                "max_age_seconds": max_age_seconds,
                "position": propagation.position_km,
                "velocity": propagation.velocity_km_s,
                "covariance": None,
                "quality": DataQuality.VALID,
                "provenance": provenance,
                "advisory_only": True,
            }
            provenance["canonical_digest"] = canonical_payload_digest(payload)
        except (AstrodynamicsError, UnicodeError, ValueError):
            return await self._ingestion.quarantine_source_failure(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                source_digest=raw_digest,
            )
        return await self._ingestion.ingest(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            payload=payload,
        )
