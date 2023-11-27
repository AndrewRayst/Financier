from fastapi import FastAPI

from src import config


application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title=config.TITLE,
    description=config.DESCRIPTION,
    version=config.VERSION,
    routes=[],
)
