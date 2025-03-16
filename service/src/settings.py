from functools import cache
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
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    DATABASE_URL: str

    @model_validator(mode="before")
    @classmethod
    def check_card_number_not_present(cls, data: dict[str, int | bool | str]) -> Any:
        database_url = data.get("DATABASE_URL")
        if database_url:
            return data
        else:
            user = data["POSTGRES_USER"]
            password = data["POSTGRES_PASSWORD"]
            host = data["POSTGRES_HOST"]
            port = data["POSTGRES_PORT"]
            db = data["POSTGRES_DB"]
            data["DATABASE_URL"] = data.get("DATABASE_URL") or (
                f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
            )
        return data


@cache
def get_settings():
    return Settings()  # type: ignore
