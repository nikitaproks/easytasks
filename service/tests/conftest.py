import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import contextlib
from typing import Any, AsyncGenerator, Awaitable, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.db.engine import Base, async_session_maker
from src.models.user import User
from src.users.auth import UserManager, get_user_db, get_user_manager
from src.users.schemas import UserCreate

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


@pytest.fixture(scope="session", autouse=True)
async def test_engine():
    from src.db.engine import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    engine.sync_engine.dispose()


@pytest.fixture(scope="function")
async def session(
    test_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture
async def user_manager(
    session: AsyncSession,
) -> AsyncGenerator[UserManager, None]:
    async with get_user_db_context(session) as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            yield user_manager


@pytest.fixture
async def user_factory(
    user_manager: UserManager,
) -> AsyncGenerator[Callable[..., Awaitable[User]], None]:
    created_users: list[User] = []

    async def create_user(**user_kwargs: dict[str, Any]) -> User:
        user = await user_manager.create(UserCreate.model_validate(user_kwargs))
        created_users.append(user)
        return user

    try:
        yield create_user
    finally:
        for user in created_users:
            await user_manager.delete(user)


@pytest.fixture
async def admin_user(
    user_factory: Callable[..., Awaitable[User]],
) -> AsyncGenerator[User, None]:
    user = await user_factory(
        email="admin@gmail.com",
        password="password",
        is_superuser=True,
        is_verified=True,
    )
    yield user


@pytest.fixture
async def regular_user(
    user_factory: Callable[..., Awaitable[User]],
) -> AsyncGenerator[User, None]:
    user = await user_factory(
        email="regular@gmail.com",
        password="password",
        is_verified=True,
    )
    yield user


@pytest.fixture
async def inactive_user(
    user_factory: Callable[..., Awaitable[User]],
) -> AsyncGenerator[User, None]:
    user = await user_factory(
        email="inactive@gmail.com",
        password="password",
        is_verified=True,
        is_active=False,
    )
    yield user


@pytest.fixture
async def unverified_user(
    user_factory: Callable[..., Awaitable[User]],
) -> AsyncGenerator[User, None]:
    user = await user_factory(
        email="unverified@gmail.com",
        password="password",
        is_verified=False,
        is_active=False,
    )
    yield user
