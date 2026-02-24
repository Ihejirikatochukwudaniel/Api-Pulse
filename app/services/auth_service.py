"""Authentication service."""
from datetime import timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(
    session: AsyncSession, email: str
) -> Optional[User]:
    """Get user by email."""
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


async def create_user(
    session: AsyncSession, user_create: UserCreate
) -> User:
    """Create a new user."""
    hashed_password = hash_password(user_create.password)
    user = User(email=user_create.email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> Optional[User]:
    """Authenticate user by email and password."""
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token_for_user(user: User) -> str:
    """Create access token for user."""
    access_token_expires = timedelta(minutes=30)
    return create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
