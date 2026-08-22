import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.db.base import Base
from ailora.domain.identity.models import Tenant, User
from ailora.domain.workflows.models import WorkflowEventRecord, WorkflowRecord, WorkflowRequest
from ailora.domain.workflows.service import IdempotencyConflictError, WorkflowService


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as value:
        tenant = Tenant(slug="workflow-tenant", display_name="Workflow Tenant")
        user = User(email="workflow@example.test", hashed_password="safe-hash")
        value.add_all([tenant, user])
        await value.flush()
        value.info["tenant_id"] = tenant.id
        value.info["user_id"] = user.id
        yield value
    await engine.dispose()


def make_request(session: AsyncSession, *, digest: str = "a" * 64) -> WorkflowRequest:
    return WorkflowRequest(
        tenant_id=session.info["tenant_id"],
        actor_user_id=session.info["user_id"],
        idempotency_key="screening-stable-001",
        workflow_type="SSA_SCREENING",
        payload_digest=digest,
        correlation_id=uuid.uuid4(),
    )


@pytest.mark.asyncio
async def test_duplicate_delivery_creates_no_second_effect(session: AsyncSession) -> None:
    service = WorkflowService(session)
    request = make_request(session)
    first, duplicate1 = await service.submit(request)
    second, duplicate2 = await service.submit(request)
    assert duplicate1 is False and duplicate2 is True and first.id == second.id
    assert (
        len(await service._repository.events(tenant_id=request.tenant_id, workflow_id=first.id))
        == 1
    )


@pytest.mark.asyncio
async def test_same_key_different_payload_is_conflict(session: AsyncSession) -> None:
    service = WorkflowService(session)
    first = make_request(session)
    await service.submit(first)
    changed = WorkflowRequest(
        tenant_id=first.tenant_id,
        actor_user_id=first.actor_user_id,
        idempotency_key=first.idempotency_key,
        workflow_type=first.workflow_type,
        payload_digest="b" * 64,
        correlation_id=first.correlation_id,
    )
    with pytest.raises(IdempotencyConflictError):
        await service.submit(changed)


def test_workflow_tables_are_registered() -> None:
    assert WorkflowRecord.__tablename__ in Base.metadata.tables
    assert WorkflowEventRecord.__tablename__ in Base.metadata.tables
