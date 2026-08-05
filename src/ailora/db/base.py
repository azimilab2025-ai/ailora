"""
AILORA SQLAlchemy declarative base.

All ORM models must inherit from `Base` defined here.
This module must not import any application-layer modules to avoid circular imports.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all AILORA ORM models."""
