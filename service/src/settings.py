import os
from typing import Any

from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file="../.env")  # type: ignore

    DEBUG: bool = False
    SECRET: str

    # Superuser
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    DATABASE_URL: str

    @model_validator(mode="before")
    @classmethod
    def check_card_number_not_present(cls, data: dict[str, int | bool | str]) -> Any:
        user = data["POSTGRES_USER"]
        password = data["POSTGRES_PASSWORD"]
        host = data["POSTGRES_HOST"]
        port = data["POSTGRES_PORT"]
        db = data["POSTGRES_DB"]

        if os.getenv("TEST", "false").lower() == "true":
            data["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
        else:
            data["DATABASE_URL"] = (
                f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
            )
        return data


settings = Settings()  # type: ignore
