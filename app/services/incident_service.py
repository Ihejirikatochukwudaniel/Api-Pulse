"""Incident service."""
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


async def create_incident(
    session: AsyncSession, incident_create: IncidentCreate
) -> Incident:
    """Create a new incident."""
    incident = Incident(**incident_create.model_dump())
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    return incident


async def get_incident(session: AsyncSession, incident_id: int) -> Optional[Incident]:
    """Get incident by ID."""
    return await session.get(Incident, incident_id)


async def list_incidents(session: AsyncSession) -> List[Incident]:
    """List all incidents."""
    statement = select(Incident)
    result = await session.execute(statement)
    return result.scalars().all()


async def resolve_incident(
    session: AsyncSession, incident_id: int
) -> Optional[Incident]:
    """Resolve an incident."""
    from datetime import datetime
    
    incident = await get_incident(session, incident_id)
    if not incident:
        return None
    
    incident.status = "resolved"
    incident.resolved_at = datetime.utcnow()
    
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    return incident
