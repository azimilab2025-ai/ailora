"""
AILORA — One-shot real tenant bootstrap (PRODUCTION SAFE)

Purpose:
  Create the first real tenant + owner user on the live database
  using the project's own repository layer and password hasher.

Safety:
  - Reads DATABASE_URL only from environment (Internal URL on Render)
  - Aborts if tenant slug or email already exists
  - No hard-coded secrets beyond the one-time owner credentials
  - Designed to be deleted after successful run

Usage (Render One-Off Job or Shell with proper env):
  python -m scripts.bootstrap_real_tenant
  or
  python scripts/bootstrap_real_tenant.py
"""

from __future__ import annotations

import asyncio
import os
import sys

# ---------------------------------------------------------------------------
# One-time owner credentials (provided by operator)
# ---------------------------------------------------------------------------
EMAIL = "azimiamin3333@yahoo.com"
PASSWORD = "Patent2025+#"
TENANT_SLUG = "oya-real"
TENANT_DISPLAY = "Oya Real Tenant"

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

async def main() -> int:
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        print("ERROR: DATABASE_URL is not set")
        return 1

    # Normalize for asyncpg if needed
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print("=" * 64)
    print("AILORA ONE-SHOT REAL TENANT BOOTSTRAP")
    print("=" * 64)
    print(f"EMAIL         = {EMAIL}")
    print(f"TENANT_SLUG   = {TENANT_SLUG}")
    print(f"DATABASE_URL  = (set, len={len(database_url)})")
    print()

    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from ailora.domain.identity.models import RoleEnum
        from ailora.domain.identity.repositories import (
            TenantRepository,
            UserRepository,
            MembershipRepository,
        )
        from ailora.security.auth import hash_password
    except Exception as exc:
        print(f"IMPORT FAILED: {exc}")
        return 1

    print("[IMPORT] OK")

    try:
        hashed = hash_password(PASSWORD)
        print(f"[HASH]   OK (len={len(hashed)})")
    except Exception as exc:
        print(f"[HASH]   FAILED: {exc}")
        return 1

    engine = create_async_engine(
        database_url,
        echo=False,
        connect_args={"ssl": "require"} if "render.com" in database_url else {},
    )
    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    try:
        async with Session() as session:
            t_repo = TenantRepository(session)
            u_repo = UserRepository(session)
            m_repo = MembershipRepository(session)

            existing_tenant = await t_repo.get_by_slug(TENANT_SLUG)
            if existing_tenant is not None:
                print(f"ABORT: tenant '{TENANT_SLUG}' already exists (id={existing_tenant.id})")
                return 2

            existing_user = await u_repo.get_by_email(EMAIL)
            if existing_user is not None:
                print(f"ABORT: email '{EMAIL}' already exists (id={existing_user.id})")
                return 3

            print("Creating Tenant ...")
            tenant = await t_repo.create(slug=TENANT_SLUG, display_name=TENANT_DISPLAY)
            print(f"  tenant.id = {tenant.id}")

            print("Creating User ...")
            user = await u_repo.create(email=EMAIL, hashed_password=hashed)
            print(f"  user.id   = {user.id}")

            print("Creating Membership (OWNER) ...")
            membership = await m_repo.create(
                user_id=user.id,
                tenant_id=tenant.id,
                role=RoleEnum.OWNER,
            )
            print(f"  membership.id = {membership.id}")

            await session.commit()

            print()
            print("SUCCESS — COMMITTED")
            print(f"  tenant_id     = {tenant.id}")
            print(f"  user_id       = {user.id}")
            print(f"  membership_id = {membership.id}")
            print(f"  role          = OWNER")
            print()
            print("You can now authenticate against the live API")
            print(f"with email={EMAIL} and the password you supplied.")
            return 0

    except Exception as exc:
        print(f"RUNTIME ERROR: {type(exc).__name__}: {exc}")
        return 1
    finally:
        await engine.dispose()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
