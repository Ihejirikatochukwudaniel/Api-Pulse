"""Incident schemas for API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IncidentBase(BaseModel):
    """Base incident schema."""

    status: str
    error_type: str


class IncidentCreate(BaseModel):
    """Schema for creating an incident."""

    monitor_id: int
    error_type: str
    status: str = "open"


class IncidentResolve(BaseModel):
    """Schema for resolving an incident."""

    pass


class IncidentResponse(IncidentBase):
    """Schema for incident response."""

    id: int
    monitor_id: int
    started_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
