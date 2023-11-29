from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src import config
from src.auth.router import router as auth_router
from src.database.core import shutdown_db


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await shutdown_db()


application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title=config.TITLE,
    description=config.DESCRIPTION,
    version=config.VERSION,
    lifespan=_lifespan,
)

application.include_router(auth_router)
