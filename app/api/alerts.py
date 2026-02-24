"""Alert API endpoints."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.alert import AlertCreate, AlertResponse, TestAlertResponse
from app.services.alert_service import create_alert, list_alerts
from app.services.simulation_service import simulate_failure

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[AlertResponse]:
    """
    List all alerts.
    """
    alerts = await list_alerts(session)
    return [AlertResponse.model_validate(a) for a in alerts]


@router.post("/test", response_model=TestAlertResponse)
async def test_alert_endpoint(
    session: AsyncSession = Depends(get_session),
) -> TestAlertResponse:
    """
    Create a test alert.
    
    This endpoint is for testing alert creation without simulating a failure.
    """
    # Create a dummy incident and alert for testing
    # First, we need to get or create a test monitor
    from app.models.monitor import Monitor
    from sqlmodel import select
    
    # Get first monitor or create a test one
    statement = select(Monitor)
    result = await session.execute(statement)
    monitor = result.scalars().first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No monitors available for test alert. Create a monitor first.",
        )
    
    # Create test payload
    test_payload: dict[str, Any] = {
        "type": "test",
        "message": "This is a test alert",
        "monitor_id": monitor.id,
        "monitor_name": monitor.name,
    }
    
    # Create a test incident and alert
    from app.models.incident import Incident
    
    incident = Incident(
        monitor_id=monitor.id,
        error_type="test",
        status="open",
    )
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    
    from app.models.alert import Alert
    
    alert = Alert(
        incident_id=incident.id,
        payload=test_payload,
    )
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    
    return TestAlertResponse(
        message="Test alert created successfully",
        alert_id=alert.id,
        alert_payload=test_payload,
    )
