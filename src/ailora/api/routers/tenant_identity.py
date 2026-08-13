"""Protected tenant identity management HTTP API."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.identity.management import (
    TenantIdentityManagementError,
    TenantIdentityManagementService,
    TenantManagementConflictError,
    TenantManagementForbiddenError,
    TenantManagementNotFoundError,
)
from ailora.domain.identity.models import Membership, RoleEnum
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix="/v1/tenants/{tenant_id}/memberships",
    tags=["Tenant Identity Management"],
)


class MembershipCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: UUID
    role: RoleEnum


class MembershipUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: RoleEnum
    is_active: bool


class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    tenant_id: UUID
    role: RoleEnum
    is_active: bool


def _authenticated_user_id(payload: dict[str, object]) -> UUID:
    subject = payload.get("sub")
    try:
        return UUID(str(subject))
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def _translate_management_error(error: TenantIdentityManagementError) -> HTTPException:
    if isinstance(error, TenantManagementForbiddenError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant management denied",
        )
    if isinstance(error, TenantManagementNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )
    if isinstance(error, TenantManagementConflictError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Tenant management denied",
    )


async def _commit_or_conflict(database: AsyncSession) -> None:
    try:
        await database.commit()
    except IntegrityError as exc:
        await database.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Membership change conflicts with existing state",
        ) from exc


@router.get("", response_model=list[MembershipResponse])
async def list_tenant_memberships(
    tenant_id: UUID,
    token_payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[Membership]:
    service = TenantIdentityManagementService(database)
    try:
        return await service.list_memberships(
            actor_user_id=_authenticated_user_id(token_payload),
            tenant_id=tenant_id,
        )
    except TenantIdentityManagementError as exc:
        raise _translate_management_error(exc) from exc


@router.post(
    "",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tenant_membership(
    tenant_id: UUID,
    request: MembershipCreateRequest,
    token_payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> Membership:
    service = TenantIdentityManagementService(database)
    try:
        membership = await service.create_membership(
            actor_user_id=_authenticated_user_id(token_payload),
            tenant_id=tenant_id,
            target_user_id=request.user_id,
            role=request.role,
        )
        await _commit_or_conflict(database)
        await database.refresh(membership)
        return membership
    except TenantIdentityManagementError as exc:
        await database.rollback()
        raise _translate_management_error(exc) from exc


@router.patch("/{membership_id}", response_model=MembershipResponse)
async def update_tenant_membership(
    tenant_id: UUID,
    membership_id: UUID,
    request: MembershipUpdateRequest,
    token_payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> Membership:
    service = TenantIdentityManagementService(database)
    try:
        membership = await service.update_membership(
            actor_user_id=_authenticated_user_id(token_payload),
            tenant_id=tenant_id,
            membership_id=membership_id,
            role=request.role,
            is_active=request.is_active,
        )
        await _commit_or_conflict(database)
        await database.refresh(membership)
        return membership
    except TenantIdentityManagementError as exc:
        await database.rollback()
        raise _translate_management_error(exc) from exc


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_tenant_membership(
    tenant_id: UUID,
    membership_id: UUID,
    token_payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    service = TenantIdentityManagementService(database)
    try:
        await service.revoke_membership(
            actor_user_id=_authenticated_user_id(token_payload),
            tenant_id=tenant_id,
            membership_id=membership_id,
        )
        await _commit_or_conflict(database)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except TenantIdentityManagementError as exc:
        await database.rollback()
        raise _translate_management_error(exc) from exc
