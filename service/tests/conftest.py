import contextlib
from typing import AsyncGenerator, Awaitable, Callable

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import Base, async_session_maker
from src.models.user import User
from src.users.auth import UserManager, get_user_db, get_user_manager
from src.users.schemas import UserCreate

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_engine():
    from src.db.engine import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def user_manager(
    session: AsyncSession,
) -> AsyncGenerator[UserManager, None]:
    async with get_user_db_context(session) as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            yield user_manager


@pytest_asyncio.fixture
async def user_factory(
    user_manager: UserManager,
) -> AsyncGenerator[Callable[..., Awaitable[User]], None]:
    created_users: list[User] = []

    async def create_user(**user_kwargs) -> User:
        user = await user_manager.create(UserCreate(**user_kwargs))
        created_users.append(user)
        return user

    try:
        yield create_user
    finally:
        for user in created_users:
            await user_manager.delete(user)


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def regular_user(
    user_factory: Callable[..., Awaitable[User]],
) -> AsyncGenerator[User, None]:
    user = await user_factory(
        email="regular@gmail.com",
        password="password",
        is_verified=True,
    )
    yield user


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
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
