"""Monitor service."""
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlmodel import select

from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate, MonitorUpdate


async def create_monitor(
    session: AsyncSession, monitor_create: MonitorCreate
) -> Monitor:
    """Create a new monitor."""
    monitor = Monitor(**monitor_create.model_dump())
    session.add(monitor)
    await session.commit()
    await session.refresh(monitor)
    return monitor


async def get_monitor(session: AsyncSession, monitor_id: int) -> Optional[Monitor]:
    """Get monitor by ID."""
    return await session.get(Monitor, monitor_id)


async def list_monitors(session: AsyncSession) -> List[Monitor]:
    """List all monitors."""
    statement = select(Monitor)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_monitor(
    session: AsyncSession, monitor_id: int, monitor_update: MonitorUpdate
) -> Optional[Monitor]:
    """Update a monitor."""
    monitor = await get_monitor(session, monitor_id)
    if not monitor:
        return None
    
    update_data = monitor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(monitor, field, value)
    
    session.add(monitor)
    await session.commit()
    await session.refresh(monitor)
    return monitor


async def delete_monitor(session: AsyncSession, monitor_id: int) -> bool:
    """Delete a monitor."""
    monitor = await get_monitor(session, monitor_id)
    if not monitor:
        return False
    
    statement = delete(Monitor).where(Monitor.id == monitor_id)
    await session.execute(statement)
    await session.commit()
    return True
