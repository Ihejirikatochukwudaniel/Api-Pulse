"""Alert schemas for API."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AlertBase(BaseModel):
    """Base alert schema."""

    payload: dict[str, Any]


class AlertCreate(AlertBase):
    """Schema for creating an alert."""

    incident_id: int


class AlertResponse(AlertBase):
    """Schema for alert response."""

    id: int
    incident_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TestAlertResponse(BaseModel):
    """Schema for test alert response."""

    message: str
    alert_id: int
    alert_payload: dict[str, Any]
