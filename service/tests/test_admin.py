from unittest.mock import AsyncMock

import pytest
from fastapi.responses import RedirectResponse

from src.admin import AdminAuthenticationBackend
from src.models.user import User
from src.users.auth import UserManager
from src.users.schemas import UserUpdate


@pytest.mark.asyncio
class TestAdminAuthenticationBackend:
    async def test_login_success(self, admin_user: User):
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        request.form.return_value = {
            "username": admin_user.email,
            "password": "password",
        }
        result = await backend.login(request)
        assert result is True
        assert "token" in request.session

    async def test_login_invalid_credentials(self, admin_user: User):
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        request.form.return_value = {
            "username": admin_user.email,
            "password": "wrong_password",
        }
        result = await backend.login(request)
        assert result is False
        assert "token" not in request.session

    async def test_login_inactive_user(
        self, user_manager: UserManager, admin_user: User
    ):
        await user_manager.update(UserUpdate(is_active=False), admin_user)
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        request.form.return_value = {
            "username": admin_user.email,
            "password": "password",
        }
        result = await backend.login(request)
        assert result is False
        assert "token" not in request.session

    async def test_login_unverified_user(
        self, user_manager: UserManager, admin_user: User
    ):
        await user_manager.update(UserUpdate(is_verified=False), admin_user)
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        request.form.return_value = {
            "username": admin_user.email,
            "password": "password",
        }
        result = await backend.login(request)
        assert result is False
        assert "token" not in request.session

    async def test_login_not_admin_user(self, regular_user: User):
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        request.form.return_value = {
            "username": regular_user.email,
            "password": "password",
        }
        result = await backend.login(request)
        assert result is False
        assert "token" not in request.session

    async def test_logout(self):
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={"token": "fake_token"})
        await backend.logout(request)
        assert "token" not in request.session

    async def test_authenticate_no_token(self):
        backend = AdminAuthenticationBackend("dummy_secret")
        request = AsyncMock(session={})
        result = await backend.authenticate(request)
        assert result is False
        assert "token" not in request.session

    async def test_authenticate_success(self, admin_user: User):
        backend = AdminAuthenticationBackend("dummy_secret")

        request = AsyncMock(session={})
        request.form.return_value = {
            "username": admin_user.email,
            "password": "password",
        }
        await backend.login(request)

        auth_request = AsyncMock(session={"token": request.session["token"]})
        result = await backend.authenticate(auth_request)
        assert result is True

    async def test_authenticate_invalid_token(self):
        backend = AdminAuthenticationBackend("dummy_secret")
        auth_request = AsyncMock(session={"token": "fake_token"})
        result = await backend.authenticate(auth_request)
        assert isinstance(
            result, RedirectResponse
        ), f"Expected RedirectResponse, got {type(result)}"
