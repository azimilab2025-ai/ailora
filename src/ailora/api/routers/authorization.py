"""Authenticated API surface for the authorization contract."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ailora.security.dependencies import require_authenticated_user

router = APIRouter(prefix="/v1/auth", tags=["Authorization"])


class AuthorizationSessionResponse(BaseModel):
    """Safe response proving that the authentication dependency succeeded."""

    authenticated: bool
    authorization_mode: str


@router.get(
    "/session",
    response_model=AuthorizationSessionResponse,
    summary="Verify the authenticated authorization session",
    description=(
        "Requires a valid bearer token. Tenant authorization remains fail-closed "
        "and must be resolved from server-side membership state."
    ),
)
async def read_authorization_session(
    authenticated_user: Annotated[object, Depends(require_authenticated_user)],
) -> AuthorizationSessionResponse:
    """Return no identity claims or secrets; dependency success is sufficient."""
    del authenticated_user
    return AuthorizationSessionResponse(
        authenticated=True,
        authorization_mode="fail_closed_tenant_membership",
    )
