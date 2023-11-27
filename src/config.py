import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

DEBUG: bool = os.getenv("DEBUG", True)
TESTING: bool = os.getenv("DEBUG", False)

TITLE: str = "Financier"
DESCRIPTION: str = "Application for financial control."
VERSION: str = "0.1.0"
