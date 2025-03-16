from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from sqladmin import Admin

from src.admin import (
    UserAdmin,
    admin_authentication_backend,
)
from src.api.auth import auth_router
from src.api.routers import version_router
from src.db.engine import engine
from src.db.tasks import create_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_superuser()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# Routers
api_router = APIRouter(prefix="/api")
api_router.include_router(version_router)
api_router.include_router(auth_router)

# App
app.include_router(api_router)

# Admin section
admin = Admin(app, engine, authentication_backend=admin_authentication_backend)
admin.add_view(UserAdmin)
