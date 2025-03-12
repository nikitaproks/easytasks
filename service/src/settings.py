from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET: str

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str

    @model_validator(mode="before")
    @classmethod
    def check_card_number_not_present(cls, data: dict[str, int | bool | str]) -> Any:
        user = data["POSTGRES_USER"]
        password = data["POSTGRES_PASSWORD"]
        host = data["POSTGRES_HOST"]
        port = data["POSTGRES_PORT"]
        db = data["POSTGRES_DB"]

        data["DATABASE_URL"] = (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        )
        data["ALEMBIC_DATABASE_URL"] = (
            f"postgresql://{user}:{password}@{host}:{port}/{db}"
        )

        return data

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore
