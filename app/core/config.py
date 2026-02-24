"""Configuration module for API Pulse."""
import os
from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings


# Resolve project base dir (two levels up from this file: app/core -> app -> project root)
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings."""

    # App
    APP_NAME: str = "API Pulse"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database: default to an absolute sqlite file under the project root
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR / 'api_pulse.db'}"

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_HOSTS: list = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
