import os

from dotenv import load_dotenv

load_dotenv()

YANDEX_S3_IMAGES_DIR: str = os.getenv("YANDEX_S3_IMAGES_DIR", "")
