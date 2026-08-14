"""Fail-closed tenant authorization and persistence for SSA scenarios."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.models import Membership, Tenant, User
from ailora.domain.shared.value_objects import TemporalStamp
from ailora.domain.ssa.scenario import ConjunctionScenario, OrbitalObjectDescriptor
from ailora.domain.ssa.scenario_models import ScenarioRecord
from ailora.domain.ssa.scenario_repository import ScenarioRepository
from ailora.security.authorization import (
    AuthorizationDeniedError,
    Permission,
    authorize_tenant_membership,
)


class ScenarioAccessDeniedError(Exception):
    """The authenticated identity cannot access the requested tenant."""


class ScenarioNotFoundError(Exception):
    """No scenario exists inside the already verified tenant boundary."""


class TenantScenarioService:
    """Creates and reads tenant-scoped, advisory-only scenario snapshots."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = ScenarioRepository(session)

    async def require_tenant_reader(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> None:
        statement = (
            select(User, Tenant, Membership)
            .join(Membership, Membership.user_id == User.id)
            .join(Tenant, Tenant.id == Membership.tenant_id)
            .where(
                User.id == actor_user_id,
                Tenant.id == tenant_id,
                Membership.user_id == actor_user_id,
                Membership.tenant_id == tenant_id,
            )
        )
        row = (await self._session.execute(statement)).one_or_none()
        if row is None:
            raise ScenarioAccessDeniedError("tenant scenario access denied")

        user, tenant, membership = row
        role = membership.role.value if hasattr(membership.role, "value") else str(membership.role)
        policy_role = {"owner": "admin", "member": "viewer"}.get(role, role)
        try:
            authorize_tenant_membership(
                authenticated_user_id=actor_user_id,
                requested_tenant_id=tenant_id,
                membership_user_id=membership.user_id,
                membership_tenant_id=membership.tenant_id,
                membership_role=policy_role,
                user_active=user.is_active,
                tenant_active=tenant.is_active,
                membership_active=membership.is_active,
                required_permission=Permission.TENANT_READ,
            )
        except AuthorizationDeniedError as exc:
            raise ScenarioAccessDeniedError("tenant scenario access denied") from exc

    async def create_scenario(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        reference_epoch: TemporalStamp,
        primary_object: OrbitalObjectDescriptor,
        secondary_object: OrbitalObjectDescriptor,
    ) -> ScenarioRecord:
        await self.require_tenant_reader(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        scenario = ConjunctionScenario(
            tenant_id=tenant_id,
            reference_epoch=reference_epoch,
            primary_object=primary_object,
            secondary_object=secondary_object,
        )
        if scenario.ADVISORY_ONLY is not True:
            raise RuntimeError("non-advisory scenario output is forbidden")

        record = ScenarioRecord(
            tenant_id=tenant_id,
            created_by_user_id=actor_user_id,
            reference_epoch=reference_epoch.model_dump(mode="json"),
            primary_object=primary_object.model_dump(mode="json"),
            secondary_object=secondary_object.model_dump(mode="json"),
            combined_classification=scenario.combined_classification.value,
            advisory_only=True,
        )
        return await self._repository.create(record)

    async def list_scenarios(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> list[ScenarioRecord]:
        await self.require_tenant_reader(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        return await self._repository.list_for_tenant(tenant_id)

    async def get_scenario(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
    ) -> ScenarioRecord:
        await self.require_tenant_reader(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        record = await self._repository.get_for_tenant(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        if record is None:
            raise ScenarioNotFoundError("scenario not found")
        return record
