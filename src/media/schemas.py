from pydantic import BaseModel

from src.schemas import SuccessResponseSchema


class MediaResponseSchema(BaseModel):
    media_id: int


class MediaLoadSuccessResponseSchema(SuccessResponseSchema):
    data: MediaResponseSchema
