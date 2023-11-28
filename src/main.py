from fastapi import FastAPI

from src import config
from src.database.core import shutdown_db

application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title=config.TITLE,
    description=config.DESCRIPTION,
    version=config.VERSION,
    routes=[],
)


@application.on_event(event_type="shutdown")
async def _shutdown() -> None:
    await shutdown_db()
