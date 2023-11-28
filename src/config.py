import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

DEBUG: bool = True if os.getenv("DEBUG", True) is True else False
TESTING: bool = True if os.getenv("DEBUG", False) is True else False

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
