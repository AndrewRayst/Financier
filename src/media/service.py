from loguru import logger
from sqlalchemy import Update, update
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


async def update_media_src(
    session: AsyncSession, media_id: int, media_src: str
) -> None:
    """
    The service for updating the src column
    in records of 'media' table by the transmitted identifiers.
    :param session: session to connect to the database.
    :param media_id: media ID for updating source
    :param media_src: new media source
    :return: None
    """
    # update image src
    statement: Update = (
        update(MediaModel).where(MediaModel.id == media_id).values(src=media_src)
    )
    await session.execute(statement)
    await session.commit()
