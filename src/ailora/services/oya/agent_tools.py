"""OYA library-agent typed tool surface.

This module defines the governed tool catalog for the OYA library agent.
All tools map exclusively to existing AILORA HTTP routes.
No external network clients, no hosted service configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass(frozen=True, slots=True)
class OyaTool:
    name: str
    path_template: str
    method: HttpMethod
    description: str


OYA_TOOL_CATALOG: Final[tuple[OyaTool, ...]] = (
    OyaTool(
        name="list_tenant_memberships",
        path_template="/v1/tenants/{tenant_id}/memberships",
        method=HttpMethod.GET,
        description="List memberships for a tenant",
    ),
    OyaTool(
        name="create_tenant_membership",
        path_template="/v1/tenants/{tenant_id}/memberships",
        method=HttpMethod.POST,
        description="Create a membership inside a tenant",
    ),
    OyaTool(
        name="update_tenant_membership",
        path_template="/v1/tenants/{tenant_id}/memberships/{membership_id}",
        method=HttpMethod.PATCH,
        description="Update an existing membership",
    ),
    OyaTool(
        name="revoke_tenant_membership",
        path_template="/v1/tenants/{tenant_id}/memberships/{membership_id}",
        method=HttpMethod.DELETE,
        description="Revoke a membership",
    ),
    OyaTool(
        name="read_authorization_session",
        path_template="/v1/auth/session",
        method=HttpMethod.GET,
        description="Verify the authenticated authorization session",
    ),
)
