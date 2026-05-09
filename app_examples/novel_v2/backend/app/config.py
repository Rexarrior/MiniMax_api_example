from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    database_url: str = Field(..., description="PostgreSQL database URL")
    secret_key: str = Field(..., min_length=32, description="Secret key for JWT/sessions (min 32 chars)")
    environment: str = Field(default="development", description="Environment: development or production")

    cors_origins: List[str] = ["http://localhost:3000"]
    stories_dir: str = "./stories"
    media_base_url: str = "/api/media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
