from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.auth.models import UserModel
from src.database.core import get_session
from src.exceptions import RequestException
from src.media.constants import ALLOWED_IMAGE_TYPES, LOADING_IMAGE, MAX_IMAGE_SIZE
from src.media.models import MediaModel
from src.media.schemas import MediaLoadSuccessResponseSchema
from src.media.service import add_media
from src.media.tasks import load_image
from src.media.utils import check_image_size, check_image_type
from src.utils import successful_response

router: APIRouter = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post("", response_model=MediaLoadSuccessResponseSchema, status_code=201)
async def _load_media(
    user: UserModel = Depends(current_user),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    """
    endpoint for adding media file.
    :param user: data of current user.
    :param file: media file for adding.
    :param session: an asynchronous session for ORM operations.
    :return: media file id.
    """
    logger.debug("checking file type.")
    await logger.complete()

    if await check_image_type(file):
        logger.debug("checking image size.")
        await logger.complete()
        if await check_image_size(file) is False:
            raise RequestException(
                f"The file is too large. Maximum size: {MAX_IMAGE_SIZE} mb."
            )

        logger.debug("adding media record to database.")
        await logger.complete()
        media: MediaModel = await add_media(
            session=session, user=user, src=LOADING_IMAGE
        )

        logger.info("creating the process of the image")
        await logger.complete()
        load_image.delay(image_id=media.id, image_data=file.file.read())

        logger.debug("returning success response.")
        await logger.complete()
        return await successful_response({"media_id": media.id}, 201)
    else:
        raise RequestException(
            f"Sorry, but our service does not work with this type of file. "
            f"Allowed image types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
