"""Monitor database model."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class Monitor(SQLModel, table=True):
    """Monitor model for tracking API endpoints."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    url: str
    expected_status_code: int = Field(default=200)
    check_interval: int = Field(default=60)  # seconds
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime)
    )
