import io
from typing import AnyStr

from fastapi import UploadFile
from PIL import Image

from src.celery_init import scoped_session
from src.media.constants import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE
from src.media.service import update_media_src


async def check_image_type(file: UploadFile) -> bool:
    """
    utility for checking image type.
    :param file: image file.
    :return: True if the file type matches.
    """
    return file.content_type in ALLOWED_IMAGE_TYPES


async def check_image_size(file: UploadFile) -> bool:
    """
    utility for checking image size.
    :param file: image file.
    :return: True if the file size matches.
    """
    size: int | None = file.size
    if size is None:
        return False

    return await convert_to_mb(size) <= MAX_IMAGE_SIZE


async def convert_to_mb(size: int) -> int:
    """
    utility to convert size from bytes to megabytes.
    :param size: size of file.
    :return: file size in megabytes.
    """
    if size <= 0:
        return 0
    return size // 1024 // 1024


def process_image(image_data: AnyStr) -> tuple[bytes, str]:
    """
    optimization images
    :param image_data: data of the image
    :return: optimized image data and image type
    """
    # loading an image data to PIL Image
    image = Image.open(io.BytesIO(image_data))  # type: ignore
    filetype: str = image.format

    # changing an image size
    image.thumbnail((600, 600), resample=Image.LANCZOS)

    # preparing to save an image
    thumb_file = io.BytesIO()
    save_args = {"format": filetype, "progressive": True}

    if image.format == "JPEG":
        save_args["quality"] = 85

    # saving an image
    image.save(thumb_file, **save_args)

    return thumb_file.getvalue(), filetype


async def update_image_src_in_database(image_id: int, image_src: str) -> None:
    """
    async update image src in the database.
    :param image_id: the image record id.
    :param image_src: new image src in storage
    :return: None
    """
    async with scoped_session() as session:
        await update_media_src(media_id=image_id, media_src=image_src, session=session)
