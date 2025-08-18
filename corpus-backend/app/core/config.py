from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Core
    environment: str = "development"
    database_url: str = "postgresql://alan:corpus_password@localhost:5432/postgres"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
