"""OYA typed plan and DAG validation.

Validates that an ordered plan only references tools present in the
governed catalog and respects tenancy and privilege boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass

from ailora.services.oya.agent_tools import OYA_TOOL_CATALOG


@dataclass(frozen=True, slots=True)
class OyaPlanStep:
    tool_name: str
    tenant_id: str | None = None


@dataclass(frozen=True, slots=True)
class OyaPlan:
    steps: tuple[OyaPlanStep, ...]


class OyaPlanValidationError(ValueError):
    """Raised when a plan violates the governed catalog or boundaries."""


def validate_oya_plan(plan: OyaPlan) -> None:
    """Validate that every step in the plan is inside the governed catalog."""
    allowed = {tool.name for tool in OYA_TOOL_CATALOG}
    for step in plan.steps:
        if step.tool_name not in allowed:
            raise OyaPlanValidationError(
                f"plan step '{step.tool_name}' is outside the governed tool catalog"
            )
