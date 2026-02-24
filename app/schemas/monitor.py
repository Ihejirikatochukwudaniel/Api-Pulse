"""Monitor schemas for API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class MonitorBase(BaseModel):
    """Base monitor schema."""

    name: str
    url: str
    expected_status_code: int = 200
    check_interval: int = 60
    is_active: bool = True


class MonitorCreate(MonitorBase):
    """Schema for creating a monitor."""

    pass


class MonitorUpdate(BaseModel):
    """Schema for updating a monitor."""

    name: Optional[str] = None
    url: Optional[str] = None
    expected_status_code: Optional[int] = None
    check_interval: Optional[int] = None
    is_active: Optional[bool] = None


class MonitorResponse(MonitorBase):
    """Schema for monitor response."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
