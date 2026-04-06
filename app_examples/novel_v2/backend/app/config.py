from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql://novel:novelpassword@localhost:5432/novel"

    secret_key: str = "dev-secret-key-change-in-production"
    cors_origins: List[str] = ["http://localhost:3000"]

    stories_dir: str = "/app/stories"

    media_base_url: str = "/api/media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
