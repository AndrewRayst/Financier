import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

DEBUG: bool = os.getenv("DEBUG", False) == "True"
TESTING: bool = os.getenv("DEBUG", False) == "True"

TITLE: str = "Financier"
DESCRIPTION: str = "Application for financial control."
VERSION: str = "0.1.0"

POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")

DB_URL: str = "postgresql+asyncpg://{}:{}@database:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)


ALEMBIC_DB_URL_DEV = (
    "postgresql+asyncpg://{}:{}@0.0.0.0:5432/{}?async_fallback=True"
).format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)

ALEMBIC_DB_URL_PROD = (
    "postgresql+asyncpg://{}:{}@database:5432/{}?async_fallback=True"
).format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)
