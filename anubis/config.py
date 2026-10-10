from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "ANUBIS"
    VERSION: str = "0.1.0"
    ANUBIS_ENV: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./anubis.db"
    
    # Redis (with local fallback if not available)
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    
    # Token Settings
    TOKEN_ALGORITHM: str = "ES256"  # ECDSA with P-256 curve
    TOKEN_DEFAULT_TTL_MINUTES: int = 15
    CHALLENGE_TTL_SECONDS: int = 120
    
    # Server signing keys (if not set in env, auto-generated on startup)
    SERVER_PRIVATE_KEY_PEM: Optional[str] = None
    SERVER_PUBLIC_KEY_PEM: Optional[str] = None
    SERVER_KID: str = "anubis-key-1"


settings = Settings()
