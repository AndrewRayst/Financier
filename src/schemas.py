from pydantic import BaseModel, fields


class SuccessResponseSchema(BaseModel):
    ok: bool = fields.Field(examples=[True])


class ErrorResponseSchema(BaseModel):
    ok: bool = fields.Field(examples=[False])
    message: str
