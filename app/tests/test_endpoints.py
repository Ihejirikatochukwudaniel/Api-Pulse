"""Test suite for API Pulse endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.database import get_session
from app.main import app
from app.schemas.user import UserCreate


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async_session_local = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_local() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """Create test client."""
    async def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to API Pulse"


@pytest.mark.asyncio
async def test_register_user(client):
    """Test user registration."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_user(client):
    """Test registering duplicate user."""
    # First registration
    await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    
    # Try duplicate registration
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client):
    """Test user login."""
    # Register first
    await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_monitor(client):
    """Test creating a monitor."""
    response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com",
            "expected_status_code": 200,
            "check_interval": 60,
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Monitor"
    assert data["url"] == "https://example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_monitors(client):
    """Test listing monitors."""
    # Create a monitor first
    await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    
    response = await client.get("/monitors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Monitor"


@pytest.mark.asyncio
async def test_get_monitor(client):
    """Test getting a specific monitor."""
    # Create a monitor first
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    response = await client.get(f"/monitors/{monitor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == monitor_id
    assert data["name"] == "Test Monitor"


@pytest.mark.asyncio
async def test_get_nonexistent_monitor(client):
    """Test getting a nonexistent monitor."""
    response = await client.get("/monitors/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_monitor(client):
    """Test deleting a monitor."""
    # Create a monitor first
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    response = await client.delete(f"/monitors/{monitor_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = await client.get(f"/monitors/{monitor_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_simulate_failure(client):
    """Test simulating a failure."""
    # Create a monitor first
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    # Simulate failure
    response = await client.post(
        f"/monitors/{monitor_id}/simulate-failure",
        json={
            "failure_type": "timeout"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["monitor_id"] == monitor_id
    assert "incident_id" in data
    assert "alert_id" in data


@pytest.mark.asyncio
async def test_list_incidents(client):
    """Test listing incidents."""
    # Create a monitor and simulate failure
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    await client.post(
        f"/monitors/{monitor_id}/simulate-failure",
        json={"failure_type": "timeout"}
    )
    
    response = await client.get("/incidents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_incident(client):
    """Test getting a specific incident."""
    # Create monitor and simulate failure
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    failure_response = await client.post(
        f"/monitors/{monitor_id}/simulate-failure",
        json={"failure_type": "timeout"}
    )
    incident_id = failure_response.json()["incident_id"]
    
    response = await client.get(f"/incidents/{incident_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident_id
    assert data["status"] == "open"


@pytest.mark.asyncio
async def test_resolve_incident(client):
    """Test resolving an incident."""
    # Create monitor and simulate failure
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    failure_response = await client.post(
        f"/monitors/{monitor_id}/simulate-failure",
        json={"failure_type": "timeout"}
    )
    incident_id = failure_response.json()["incident_id"]
    
    response = await client.post(
        f"/incidents/{incident_id}/resolve",
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "resolved"


@pytest.mark.asyncio
async def test_list_alerts(client):
    """Test listing alerts."""
    # Create monitor and simulate failure
    create_response = await client.post(
        "/monitors",
        json={
            "name": "Test Monitor",
            "url": "https://example.com"
        }
    )
    monitor_id = create_response.json()["id"]
    
    await client.post(
        f"/monitors/{monitor_id}/simulate-failure",
        json={"failure_type": "timeout"}
    )
    
    response = await client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
