import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

DEBUG: bool = True if os.getenv("DEBUG", True) is True else False
TESTING: bool = True if os.getenv("DEBUG", False) is True else False

TITLE: str = "Financier"
DESCRIPTION: str = "Application for financial control."
VERSION: str = "0.1.0"
