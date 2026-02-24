"""Simulation service for deterministic failure testing."""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.models.monitor import Monitor
from app.schemas.alert import AlertCreate
from app.schemas.incident import IncidentCreate
from app.services.alert_service import create_alert
from app.services.incident_service import create_incident
from app.services.monitor_service import get_monitor


async def simulate_failure(
    session: AsyncSession,
    monitor_id: int,
    failure_type: str,
    latency_ms: Optional[int] = None,
) -> dict:
    """
    Simulate a failure for a monitor.
    
    This is deterministic and repeatable for demo purposes.
    """
    # Validate monitor exists
    monitor = await get_monitor(session, monitor_id)
    if not monitor:
        return {
            "success": False,
            "error": "Monitor not found",
            "monitor_id": monitor_id,
        }
    
    # Create incident
    incident_create = IncidentCreate(
        monitor_id=monitor_id,
        error_type=failure_type,
        status="open",
    )
    incident = await create_incident(session, incident_create)
    
    # Create alert with payload
    alert_payload = {
        "incident_id": incident.id,
        "monitor_id": monitor_id,
        "monitor_name": monitor.name,
        "monitor_url": monitor.url,
        "failure_type": failure_type,
        "latency_ms": latency_ms,
        "message": f"Monitor '{monitor.name}' encountered a {failure_type} failure",
    }
    
    alert_create = AlertCreate(
        incident_id=incident.id,
        payload=alert_payload,
    )
    alert = await create_alert(session, alert_create)
    
    return {
        "success": True,
        "monitor_id": monitor_id,
        "monitor_name": monitor.name,
        "incident_id": incident.id,
        "incident_status": incident.status,
        "alert_id": alert.id,
        "payload": alert_payload,
    }
