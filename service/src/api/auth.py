from fastapi import APIRouter
from src.users.auth import (
    auth_backend,
    fastapi_users,
)
from src.users.schemas import UserCreate, UserRead

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)
