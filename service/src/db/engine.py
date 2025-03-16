from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import get_settings

DATABASE_URL = get_settings().DATABASE_URL
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    engine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore
