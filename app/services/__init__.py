"""Services module initialization."""
from app.services.alert_service import (
    create_alert,
    get_alert,
    list_alerts,
)
from app.services.auth_service import (
    authenticate_user,
    create_user,
    create_access_token_for_user,
    get_user_by_email,
)
from app.services.incident_service import (
    create_incident,
    get_incident,
    list_incidents,
    resolve_incident,
)
from app.services.monitor_service import (
    create_monitor,
    delete_monitor,
    get_monitor,
    list_monitors,
    update_monitor,
)
from app.services.simulation_service import simulate_failure

__all__ = [
    "create_user",
    "get_user_by_email",
    "authenticate_user",
    "create_access_token_for_user",
    "create_monitor",
    "get_monitor",
    "list_monitors",
    "update_monitor",
    "delete_monitor",
    "create_incident",
    "get_incident",
    "list_incidents",
    "resolve_incident",
    "create_alert",
    "get_alert",
    "list_alerts",
    "simulate_failure",
]
