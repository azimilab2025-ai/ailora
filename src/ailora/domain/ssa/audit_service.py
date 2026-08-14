"""Fail-closed append-only audit service for tenant SSA evidence."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.models import Membership, Tenant, User
from ailora.domain.ssa.audit import AuditEntry, AuditEventType
from ailora.domain.ssa.audit_models import AuditEventRecord
from ailora.domain.ssa.audit_repository import AuditEventRepository
from ailora.security.authorization import (
    AuthorizationDeniedError,
    Permission,
    authorize_tenant_membership,
)


class AuditAccessDeniedError(Exception):
    """The authenticated identity cannot read audit evidence for the tenant."""


class AuditEventNotFoundError(Exception):
    """No audit event exists inside the verified tenant boundary."""


class AuditInputError(ValueError):
    """Audit evidence violates the bounded, secret-safe contract."""


class TenantAuditService:
    """Appends internal events and exposes tenant-filtered immutable reads."""

    _RESOURCE_TYPES = frozenset({"scenario", "screening", "risk_assessment", "review"})

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = AuditEventRepository(session)

    async def require_tenant_reader(
        self, *, actor_user_id: uuid.UUID, tenant_id: uuid.UUID
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
            raise AuditAccessDeniedError("tenant audit access denied")
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
            raise AuditAccessDeniedError("tenant audit access denied") from exc

    async def append_event(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        event_type: AuditEventType,
        resource_type: str,
        resource_id: uuid.UUID,
        combined_classification: str,
        outcome: str = "SUCCESS",
        correlation_id: uuid.UUID | None = None,
        detail: str = "",
    ) -> AuditEventRecord:
        if resource_type not in self._RESOURCE_TYPES:
            raise AuditInputError("unsupported audit resource type")
        if not combined_classification or len(combined_classification) > 32:
            raise AuditInputError("invalid audit classification")
        if len(detail) > 1000:
            raise AuditInputError("audit detail exceeds 1000 characters")
        correlation = correlation_id or uuid.uuid4()
        try:
            entry = AuditEntry.create(
                tenant_id=tenant_id,
                actor_id=actor_user_id,
                event_type=event_type,
                resource_id=str(resource_id),
                outcome=outcome,
                correlation_id=str(correlation),
                detail=detail,
            )
        except ValueError as exc:
            raise AuditInputError("audit text rejected by secret-safety policy") from exc
        return await self._repository.append(
            AuditEventRecord(
                id=entry.entry_id,
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                event_type=event_type.value,
                resource_type=resource_type,
                resource_id=resource_id,
                outcome=outcome,
                correlation_id=correlation,
                detail=detail,
                combined_classification=combined_classification,
                advisory_only=True,
                timestamp_utc=entry.timestamp_utc,
            )
        )

    async def list_events(
        self, *, actor_user_id: uuid.UUID, tenant_id: uuid.UUID
    ) -> list[AuditEventRecord]:
        await self.require_tenant_reader(actor_user_id=actor_user_id, tenant_id=tenant_id)
        return await self._repository.list_for_tenant(tenant_id)

    async def get_event(
        self, *, actor_user_id: uuid.UUID, tenant_id: uuid.UUID, event_id: uuid.UUID
    ) -> AuditEventRecord:
        await self.require_tenant_reader(actor_user_id=actor_user_id, tenant_id=tenant_id)
        record = await self._repository.get_for_tenant(tenant_id=tenant_id, event_id=event_id)
        if record is None:
            raise AuditEventNotFoundError("audit event not found")
        return record
