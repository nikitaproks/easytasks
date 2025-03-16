import contextlib
from typing import cast

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import Response

from src.db.generators import get_async_session, get_user_db
from src.models.user import User
from src.settings import get_settings
from src.users.auth import get_jwt_strategy, get_user_manager

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


class UserAdmin(ModelView, model=User):
    column_list = [str(User.id), User.email]


class AdminAuthenticationBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = cast(str, form["username"])
        password = cast(str, form["password"])

        user: User | None = None
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.authenticate(
                        OAuth2PasswordRequestForm(username=username, password=password)
                    )
        print(user)
        if (
            user is None
            or not user.is_active
            or not user.is_verified
            or not user.is_superuser
        ):
            return False

        strategy = get_jwt_strategy()
        token = await strategy.write_token(user)

        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("token")
        if not token:
            return False

        strategy = get_jwt_strategy()
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    try:
                        user = await strategy.read_token(token, user_manager)
                        if user:
                            return True
                    except Exception:
                        pass
        return RedirectResponse(url="/admin/login")


admin_authentication_backend = AdminAuthenticationBackend(get_settings().SECRET)
