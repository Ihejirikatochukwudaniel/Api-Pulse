"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token_for_user,
    create_user,
    get_user_by_email,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Register a new user.
    
    - **email**: User email address
    - **password**: User password
    """
    # Check if user already exists
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = await create_user(session, user_create)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """
    Login with email and password.
    
    - **email**: User email address
    - **password**: User password
    
    Returns access token for authenticated requests.
    """
    user = await authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token_for_user(user)
    return TokenResponse(access_token=access_token)
