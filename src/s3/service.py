from typing import AnyStr

from loguru import logger

from src import config
from src.s3 import config as s3_config
from src.s3.client import Client
from src.s3.utils import get_unique_filename


def send_file_to_storage(file_data: AnyStr, filetype: str, dir_path: str) -> str:
    """
    service for loading file to yandex s3 storage.
    :param file_data: data of the file.
    :param filetype: type of file.
    :param dir_path: path of directory.
    :return: the file src in storage
    """
    # sending image to storage and getting src
    if config.TESTING or config.DEBUG:
        return "file_src_test"

    filename = get_unique_filename(filetype)

    with Client() as client:
        response = client.put_object(
            Bucket=s3_config.YANDEX_S3_BUCKET_NAME,
            Key=dir_path + filename,
            Body=file_data,
        )

        status_code: int = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status_code != 200:
            logger.warning("file upload failed")

        return config.YANDEX_S3_BUCKET_URL + dir_path + filename
