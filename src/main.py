from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator, Callable

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src import config
from src.auth.router import router as auth_router
from src.database.core import shutdown_db
from src.exceptions import CustomException
from src.media.router import router as media_router
from src.utils import exception_response, server_exception_response

logger.add(
    f"../logs/{datetime.now().strftime('%Y-%m-%d')}_log.json",
    level="INFO",
    format="{level} {time} {message}",
    serialize=True,
    rotation="00:00",
    compression="zip",
)


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.debug("starting...")
    await logger.complete()
    yield
    await shutdown_db()


application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title=config.TITLE,
    description=config.DESCRIPTION,
    version=config.VERSION,
    lifespan=_lifespan,
)

api_router: APIRouter = APIRouter(prefix="/api")
api_router.include_router(media_router)

application.include_router(auth_router)
application.include_router(api_router)


@application.exception_handler(CustomException)
async def _exception_handler(_: Request, exception: CustomException) -> JSONResponse:
    logger.exception(exception)
    await logger.complete()
    return await exception_response(exception)


@application.middleware("http")
async def _catch_unhandled_errors(
    request: Request, call_next: Callable
) -> JSONResponse:
    try:
        return await call_next(request)
    except Exception as error:
        logger.error(error)
        await logger.complete()
        return await server_exception_response()
