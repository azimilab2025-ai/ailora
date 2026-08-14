"""Read-only authenticated API for tenant-scoped SSA audit evidence."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.ssa.audit_models import AuditEventRecord
from ailora.domain.ssa.audit_service import (
    AuditAccessDeniedError,
    AuditEventNotFoundError,
    TenantAuditService,
)
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix="/v1/tenants/{tenant_id}/ssa/audit-events",
    tags=["ssa-audit"],
    dependencies=[Depends(require_authenticated_user)],
)


class AuditEventResponse(BaseModel):
    """Secret-safe immutable audit evidence returned to authorized readers."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    tenant_id: UUID
    actor_user_id: UUID
    event_type: str
    resource_type: str
    resource_id: UUID
    outcome: str
    correlation_id: UUID
    detail: str
    combined_classification: str
    advisory_only: bool
    timestamp_utc: datetime

    @classmethod
    def from_record(cls, record: AuditEventRecord) -> AuditEventResponse:
        return cls.model_validate(record, from_attributes=True)


def _actor_user_id(payload: dict[str, object]) -> UUID:
    subject = payload.get("sub")
    try:
        return UUID(str(subject))
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def _translate_error(error: Exception) -> HTTPException:
    if isinstance(error, AuditAccessDeniedError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Tenant audit access denied"
        )
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit event not found")


@router.get("", response_model=list[AuditEventResponse])
async def list_audit_events(
    tenant_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[AuditEventResponse]:
    try:
        records = await TenantAuditService(database).list_events(
            actor_user_id=_actor_user_id(payload), tenant_id=tenant_id
        )
        return [AuditEventResponse.from_record(record) for record in records]
    except AuditAccessDeniedError as exc:
        raise _translate_error(exc) from exc


@router.get("/{event_id}", response_model=AuditEventResponse)
async def read_audit_event(
    tenant_id: UUID,
    event_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> AuditEventResponse:
    try:
        record = await TenantAuditService(database).get_event(
            actor_user_id=_actor_user_id(payload), tenant_id=tenant_id, event_id=event_id
        )
        return AuditEventResponse.from_record(record)
    except (AuditAccessDeniedError, AuditEventNotFoundError) as exc:
        raise _translate_error(exc) from exc
