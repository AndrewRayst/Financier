import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

DEBUG: bool = os.getenv("DEBUG", False) == "True"
TESTING: bool = os.getenv("TESTING", False) == "True"

TITLE: str = "Financier"
DESCRIPTION: str = "Application for financial control."
VERSION: str = "0.1.0"

POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "0.0.0.0")

DB_URL: str = "postgresql+asyncpg://{}:{}@database:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)

DB_URL_TEST: str = "postgresql+asyncpg://{}:{}@{}:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
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


REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
REDIS_USER: str = os.getenv("REDIS_USER", "")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

REDIS_URL: str = (
    f"redis://0.0.0.0:{REDIS_PORT}"
    if TESTING
    else f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
)

MANAGER_SECRET: str = os.getenv("MANAGER_SECRET", "")
