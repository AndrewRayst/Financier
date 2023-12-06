from types import TracebackType
from typing import Optional

from boto3.session import Session
from botocore.client import BaseClient
from loguru import logger

from src import config


class Client:
    """
    client for connection to s3.
    """

    __session: Session = Session(
        aws_access_key_id=config.YANDEX_S3_ACCESS_KEY_ID,
        aws_secret_access_key=config.YANDEX_S3_SECRET_ACCESS_KEY,
        region_name=config.YANDEX_S3_REGION_NAME,
    )

    def __init__(
        self,
        endpoint_url: str = config.YANDEX_S3_ENDPOINT,
        service_name: str = "s3",
    ) -> None:
        self.__endpoint_url: str = endpoint_url
        self.__service_name: str = service_name

    def __enter__(self) -> BaseClient:
        logger.debug("creating s3 client.")
        self.__client: BaseClient = self.__session.client(
            service_name=self.__service_name, endpoint_url=self.__endpoint_url
        )
        return self.__client

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            logger.warning(
                f"exc_type: {exc_type}\n exc_val: {exc_val}\n exc_tb: {exc_tb}"
            )

        logger.debug("closing s3 client.")
        self.__client.close()
