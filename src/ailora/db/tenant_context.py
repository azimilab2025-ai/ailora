"""Fail-closed PostgreSQL transaction context for tenant-scoped requests."""

from dataclasses import dataclass
from typing import Final
from uuid import UUID, uuid4

from fastapi import Request
from sqlalchemy import Connection, event, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, SessionTransaction

SESSION_CONTEXT_KEY: Final = "ailora_tenant_database_context"


@dataclass(frozen=True, slots=True)
class TenantDatabaseContext:
    """Immutable request identity and bounded database execution budgets."""

    tenant_id: UUID | None
    actor_id: UUID | None
    correlation_id: UUID
    statement_timeout_ms: int
    lock_timeout_ms: int
    idle_transaction_timeout_ms: int


def _optional_uuid(value: object) -> UUID | None:
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        try:
            return UUID(value)
        except ValueError:
            return None
    return None


def context_from_request(
    request: Request,
    *,
    statement_timeout_ms: int,
    lock_timeout_ms: int,
    idle_transaction_timeout_ms: int,
) -> TenantDatabaseContext:
    """Derive untrusted path identity and trusted middleware correlation context."""
    tenant_id = _optional_uuid(request.path_params.get("tenant_id"))
    actor_id = _optional_uuid(getattr(request.state, "actor_id", None))
    correlation_id = _optional_uuid(getattr(request.state, "correlation_id", None)) or uuid4()
    return TenantDatabaseContext(
        tenant_id=tenant_id,
        actor_id=actor_id,
        correlation_id=correlation_id,
        statement_timeout_ms=statement_timeout_ms,
        lock_timeout_ms=lock_timeout_ms,
        idle_transaction_timeout_ms=idle_transaction_timeout_ms,
    )


def transaction_settings(context: TenantDatabaseContext) -> tuple[tuple[str, str], ...]:
    """Return transaction-local settings without emitting SQL."""
    return (
        ("app.current_tenant_id", str(context.tenant_id) if context.tenant_id else ""),
        ("app.current_actor_id", str(context.actor_id) if context.actor_id else ""),
        ("app.correlation_id", str(context.correlation_id)),
        ("statement_timeout", f"{context.statement_timeout_ms}ms"),
        ("lock_timeout", f"{context.lock_timeout_ms}ms"),
        (
            "idle_in_transaction_session_timeout",
            f"{context.idle_transaction_timeout_ms}ms",
        ),
    )


def configure_session_context(session: AsyncSession, context: TenantDatabaseContext) -> None:
    """Attach request context for reapplication at every transaction boundary."""
    session.sync_session.info[SESSION_CONTEXT_KEY] = context


def clear_session_context(session: AsyncSession) -> None:
    """Remove request context before a pooled session can be discarded."""
    session.sync_session.info.pop(SESSION_CONTEXT_KEY, None)


@event.listens_for(Session, "after_begin")
def _apply_postgres_transaction_context(
    session: Session,
    transaction: SessionTransaction,
    connection: Connection,
) -> None:
    """Apply tenant identity and budgets with PostgreSQL transaction-local scope."""
    del transaction
    context = session.info.get(SESSION_CONTEXT_KEY)
    if not isinstance(context, TenantDatabaseContext):
        return
    if connection.dialect.name != "postgresql":
        return

    statement = text("SELECT set_config(:setting_name, :setting_value, true)")
    for setting_name, setting_value in transaction_settings(context):
        connection.execute(
            statement,
            {"setting_name": setting_name, "setting_value": setting_value},
        )
