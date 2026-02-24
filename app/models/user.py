"""User database model."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime)
    )
