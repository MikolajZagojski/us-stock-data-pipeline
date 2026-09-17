from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    api_key: str = Field(..., alias="API_KEY")

    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: int = Field(5433, alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_pass: str = Field(..., alias="DB_PASS")


@lru_cache
def get_settings() -> Settings:
    return Settings()