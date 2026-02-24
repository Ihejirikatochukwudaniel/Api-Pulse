"""Incident database model."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class Incident(SQLModel, table=True):
    """Incident model for tracking failures."""

    id: Optional[int] = Field(default=None, primary_key=True)
    monitor_id: int = Field(foreign_key="monitor.id", index=True)
    status: str = Field(default="open", index=True)  # open, resolved
    error_type: str  # timeout, 500, latency
    started_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime)
    )
    resolved_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime)
    )
