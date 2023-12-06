import asyncio
from typing import AnyStr

from loguru import logger

from src.celery_init import celery_app, scoped_session
from src.media import config as media_config
from src.media.service import update_media_src
from src.media.utils import process_image
from src.s3.service import send_file_to_storage


@celery_app.task
def load_image(image_id: int, image_data: AnyStr) -> None:
    """
    task for load image to the storage and update src in the database
    :param image_id: the image record id.
    :param image_data: data of the images
    :return: None
    """
    logger.debug("optimizing image")
    # optimizing image
    image, filetype = process_image(image_data=image_data)

    logger.debug("sending image to storage")
    # sending image to storage
    image_src: str = send_file_to_storage(
        file_data=image,
        filetype=filetype.lower(),
        dir_path=media_config.YANDEX_S3_IMAGES_DIR,
    )

    logger.debug("updating image source in database")
    # updating image source in database
    asyncio.get_event_loop().run_until_complete(
        update_image_src_in_database(image_id=image_id, image_src=image_src)
    )


async def update_image_src_in_database(image_id: int, image_src: str) -> None:
    """
    async update image src in the database.
    :param image_id: the image record id.
    :param image_src: new image src in storage
    :return: None
    """
    async with scoped_session() as session:
        await update_media_src(media_id=image_id, media_src=image_src, session=session)
