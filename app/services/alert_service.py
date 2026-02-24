"""Alert service."""
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.alert import Alert
from app.schemas.alert import AlertCreate


async def create_alert(
    session: AsyncSession, alert_create: AlertCreate
) -> Alert:
    """Create a new alert."""
    alert = Alert(**alert_create.model_dump())
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    return alert


async def get_alert(session: AsyncSession, alert_id: int) -> Optional[Alert]:
    """Get alert by ID."""
    return await session.get(Alert, alert_id)


async def list_alerts(session: AsyncSession) -> List[Alert]:
    """List all alerts."""
    statement = select(Alert)
    result = await session.execute(statement)
    return result.scalars().all()
