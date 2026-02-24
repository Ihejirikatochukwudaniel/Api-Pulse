"""Demo data seeding script."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session, init_db
from app.core.logging import logger
from app.schemas.monitor import MonitorCreate
from app.schemas.user import UserCreate
from app.services.auth_service import create_user
from app.services.monitor_service import create_monitor
from app.services.simulation_service import simulate_failure


async def seed_database():
    """Seed the database with demo data."""
    logger.info("Starting database seeding...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    async with async_session() as session:
        try:
            # Create demo user
            logger.info("Creating demo user...")
            demo_user = UserCreate(
                email="demo@apipulse.local",
                password="demo123"
            )
            user = await create_user(session, demo_user)
            logger.info(f"✓ Created demo user: {user.email}")
            
            # Create monitors
            logger.info("Creating monitors...")
            monitor1_data = MonitorCreate(
                name="Google API",
                url="https://www.google.com",
                expected_status_code=200,
                check_interval=60,
                is_active=True,
            )
            monitor1 = await create_monitor(session, monitor1_data)
            logger.info(f"✓ Created monitor: {monitor1.name} (ID: {monitor1.id})")
            
            monitor2_data = MonitorCreate(
                name="GitHub API",
                url="https://api.github.com",
                expected_status_code=200,
                check_interval=120,
                is_active=True,
            )
            monitor2 = await create_monitor(session, monitor2_data)
            logger.info(f"✓ Created monitor: {monitor2.name} (ID: {monitor2.id})")
            
            # Simulate failures
            logger.info("Simulating failures...")
            
            # Simulate timeout failure for monitor1
            failure1 = await simulate_failure(
                session,
                monitor1.id,
                "timeout",
                latency_ms=None,
            )
            logger.info(f"✓ Simulated timeout failure for {monitor1.name}")
            logger.info(f"  Incident ID: {failure1['incident_id']}")
            logger.info(f"  Alert ID: {failure1['alert_id']}")
            
            # Simulate 500 error for monitor2
            failure2 = await simulate_failure(
                session,
                monitor2.id,
                "500",
                latency_ms=None,
            )
            logger.info(f"✓ Simulated 500 error for {monitor2.name}")
            logger.info(f"  Incident ID: {failure2['incident_id']}")
            logger.info(f"  Alert ID: {failure2['alert_id']}")
            
            # Simulate latency issue for monitor1
            failure3 = await simulate_failure(
                session,
                monitor1.id,
                "latency",
                latency_ms=5000,
            )
            logger.info(f"✓ Simulated latency failure for {monitor1.name}")
            logger.info(f"  Incident ID: {failure3['incident_id']}")
            logger.info(f"  Alert ID: {failure3['alert_id']}")
            
            logger.info("\n" + "="*60)
            logger.info("✓ Database seeding completed successfully!")
            logger.info("="*60)
            logger.info("\nDemo data created:")
            logger.info(f"  User: demo@apipulse.local / demo123")
            logger.info(f"  Monitors: {monitor1.name}, {monitor2.name}")
            logger.info(f"  Incidents: 3 simulated failures")
            logger.info("\nYou can now start the server with:")
            logger.info("  uvicorn app.main:app --reload")
            
        except Exception as e:
            logger.error(f"✗ Error seeding database: {str(e)}", exc_info=True)
            raise


def main():
    """Entry point."""
    asyncio.run(seed_database())


if __name__ == "__main__":
    main()
