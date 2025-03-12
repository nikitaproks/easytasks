from fastapi import APIRouter
from src.users.auth import (
    fastapi_users,
)
from src.users.schemas import UserRead, UserUpdate

user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
