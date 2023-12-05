from fastapi import UploadFile

from src.media.constants import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE


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
