"""Fail-closed tenant service for advisory T0/PHY-C1 screening."""

from __future__ import annotations

import math
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.shared.value_objects import CartesianState, TemporalStamp
from ailora.domain.ssa.audit import AuditEventType
from ailora.domain.ssa.audit_service import TenantAuditService
from ailora.domain.ssa.scenario_models import ScenarioRecord
from ailora.domain.ssa.scenario_service import TenantScenarioService
from ailora.domain.ssa.screening import screen_t0_phy_c1
from ailora.domain.ssa.screening_models import ScreeningRecord
from ailora.domain.ssa.screening_repository import ScreeningRepository


class ScreeningNotFoundError(Exception):
    """No screening exists inside the verified tenant and scenario boundary."""


class ScreeningInputError(ValueError):
    """Screening states violate the bounded T0/PHY-C1 input contract."""


class TenantScreeningService:
    """Runs and reads tenant-scoped, advisory-only screening snapshots."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._scenario_service = TenantScenarioService(session)
        self._repository = ScreeningRepository(session)

    @staticmethod
    def _same_temporal_context(left: TemporalStamp, right: TemporalStamp) -> bool:
        return left.epoch.utc == right.epoch.utc and left.frame == right.frame

    @classmethod
    def _validate_states(
        cls,
        *,
        scenario: ScenarioRecord,
        primary_state: CartesianState,
        secondary_state: CartesianState,
        threshold_km: float,
    ) -> None:
        if not math.isfinite(threshold_km) or threshold_km <= 0:
            raise ScreeningInputError("threshold_km must be finite and greater than zero")
        if not cls._same_temporal_context(primary_state.stamp, secondary_state.stamp):
            raise ScreeningInputError(
                "primary and secondary states must share epoch and reference frame"
            )
        scenario_stamp = TemporalStamp.model_validate(scenario.reference_epoch)
        if not cls._same_temporal_context(primary_state.stamp, scenario_stamp):
            raise ScreeningInputError(
                "screening states must match the persisted scenario temporal context"
            )

    async def create_screening(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        primary_state: CartesianState,
        secondary_state: CartesianState,
        threshold_km: float,
    ) -> ScreeningRecord:
        scenario = await self._scenario_service.get_scenario(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        self._validate_states(
            scenario=scenario,
            primary_state=primary_state,
            secondary_state=secondary_state,
            threshold_km=threshold_km,
        )
        result = screen_t0_phy_c1(
            primary_state,
            secondary_state,
            conjunction_distance_threshold_km=threshold_km,
        )
        if result.is_advisory is not True:
            raise RuntimeError("non-advisory screening output is forbidden")

        record = ScreeningRecord(
            tenant_id=tenant_id,
            scenario_id=scenario.id,
            created_by_user_id=actor_user_id,
            primary_state=primary_state.model_dump(mode="json"),
            secondary_state=secondary_state.model_dump(mode="json"),
            threshold_km=result.threshold_km,
            tier=result.tier.value,
            outcome=result.outcome.value,
            distance_km=result.distance_km,
            combined_classification=scenario.combined_classification,
            advisory_only=True,
            advisory_statement=result.advisory_statement,
        )
        record = await self._repository.create(record)
        await TenantAuditService(self._session).append_event(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=AuditEventType.SCENARIO_SCREENED,
            resource_type="screening",
            resource_id=record.id,
            combined_classification=record.combined_classification,
            detail="Advisory T0 PHY-C1 screening created",
        )
        return record

    async def list_screenings(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
    ) -> list[ScreeningRecord]:
        scenario = await self._scenario_service.get_scenario(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        return await self._repository.list_for_tenant_scenario(
            tenant_id=tenant_id,
            scenario_id=scenario.id,
        )

    async def get_screening(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
    ) -> ScreeningRecord:
        scenario = await self._scenario_service.get_scenario(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        record = await self._repository.get_for_tenant_scenario(
            tenant_id=tenant_id,
            scenario_id=scenario.id,
            screening_id=screening_id,
        )
        if record is None:
            raise ScreeningNotFoundError("screening not found")
        return record
