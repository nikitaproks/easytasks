from fastapi import APIRouter, FastAPI

from src.api.auth import auth_router
from src.api.routers import version_router

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


api_router = APIRouter(prefix="/api")
api_router.include_router(version_router)
api_router.include_router(auth_router)


app.include_router(api_router)
