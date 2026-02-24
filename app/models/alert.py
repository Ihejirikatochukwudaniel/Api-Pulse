"""Alert database model."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlmodel import Column, DateTime, Field, JSON, SQLModel


class Alert(SQLModel, table=True):
    """Alert model for tracking notifications."""

    id: Optional[int] = Field(default=None, primary_key=True)
    incident_id: int = Field(foreign_key="incident.id", index=True)
    payload: dict[str, Any] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime)
    )
