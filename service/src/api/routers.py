from fastapi import APIRouter
from src.api.v1.users import user_router

version_router = APIRouter()
version_router.include_router(prefix="/v1", router=user_router)
