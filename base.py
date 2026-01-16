"""
SQLAlchemy declarative base and common mixins.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base, declared_attr
import uuid


# Declarative base for all ORM models
Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class TableNameMixin:
    """Mixin to automatically set table name from class name."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name (convert CamelCase to snake_case)."""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
