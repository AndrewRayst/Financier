from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel
from src.media.models import MediaModel


async def add_media(session: AsyncSession, user: UserModel, src: str) -> MediaModel:
    """
    service for adding media record to database.
    :param session: an asynchronous session for ORM operations.
    :param user: user who wants to add media.
    :param src: media file src.
    :return: instance of media with id.
    """
    instance: MediaModel = MediaModel(src=src, user_id=user.id)
    session.add(instance)
    await session.commit()

    logger.info(f"media record added to database with id: {instance.id}.")
    await logger.complete()

    return instance
