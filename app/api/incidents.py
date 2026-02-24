"""Incident API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.incident import IncidentResponse, IncidentResolve
from app.services.incident_service import (
    get_incident,
    list_incidents,
    resolve_incident,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentResponse])
async def list_incidents_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[IncidentResponse]:
    """
    List all incidents.
    """
    incidents = await list_incidents(session)
    return [IncidentResponse.model_validate(i) for i in incidents]


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident_endpoint(
    incident_id: int,
    session: AsyncSession = Depends(get_session),
) -> IncidentResponse:
    """
    Get a specific incident by ID.
    
    - **incident_id**: Incident ID
    """
    incident = await get_incident(session, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    return IncidentResponse.model_validate(incident)


@router.post("/{incident_id}/resolve", response_model=IncidentResponse)
async def resolve_incident_endpoint(
    incident_id: int,
    _: IncidentResolve,
    session: AsyncSession = Depends(get_session),
) -> IncidentResponse:
    """
    Resolve an incident.
    
    - **incident_id**: Incident ID
    """
    incident = await resolve_incident(session, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    return IncidentResponse.model_validate(incident)
