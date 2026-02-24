"""Monitor API endpoints."""
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.monitor import MonitorCreate, MonitorResponse, MonitorUpdate
from app.services.monitor_service import (
    create_monitor,
    delete_monitor,
    get_monitor,
    list_monitors,
    update_monitor,
)
from app.services.simulation_service import simulate_failure

router = APIRouter(prefix="/monitors", tags=["monitors"])


@router.post("", response_model=MonitorResponse, status_code=status.HTTP_201_CREATED)
async def create_monitor_endpoint(
    monitor_create: MonitorCreate,
    session: AsyncSession = Depends(get_session),
) -> MonitorResponse:
    """
    Create a new monitor.
    
    - **name**: Monitor name
    - **url**: API endpoint URL to monitor
    - **expected_status_code**: Expected HTTP status code (default: 200)
    - **check_interval**: Check interval in seconds (default: 60)
    - **is_active**: Whether monitor is active (default: true)
    """
    monitor = await create_monitor(session, monitor_create)
    return MonitorResponse.model_validate(monitor)


@router.get("", response_model=list[MonitorResponse])
async def list_monitors_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[MonitorResponse]:
    """
    List all monitors.
    """
    monitors = await list_monitors(session)
    return [MonitorResponse.model_validate(m) for m in monitors]


@router.get("/{monitor_id}", response_model=MonitorResponse)
async def get_monitor_endpoint(
    monitor_id: int,
    session: AsyncSession = Depends(get_session),
) -> MonitorResponse:
    """
    Get a specific monitor by ID.
    
    - **monitor_id**: Monitor ID
    """
    monitor = await get_monitor(session, monitor_id)
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )
    return MonitorResponse.model_validate(monitor)


@router.delete("/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monitor_endpoint(
    monitor_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a monitor.
    
    - **monitor_id**: Monitor ID
    """
    success = await delete_monitor(session, monitor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )


class SimulateFailurePayload(BaseModel):
    """Payload for simulating failure."""

    failure_type: str
    latency_ms: int | None = None


@router.post("/{monitor_id}/simulate-failure", status_code=status.HTTP_201_CREATED)
async def simulate_failure_endpoint(
    monitor_id: int,
    payload: SimulateFailurePayload,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Simulate a failure for a monitor.
    
    This creates an incident and alert deterministically for testing.
    
    - **monitor_id**: Monitor ID
    - **failure_type**: Type of failure (timeout, 500, latency, etc.)
    - **latency_ms**: Optional latency in milliseconds
    """
    result = await simulate_failure(
        session,
        monitor_id,
        payload.failure_type,
        payload.latency_ms,
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("error", "Failed to simulate failure"),
        )
    
    return result
