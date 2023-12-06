from fastapi.responses import JSONResponse

from src.exceptions import CustomException


async def successful_response(data: dict, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        content={
            "ok": True,
            "data": data,
        },
        status_code=status_code,
    )


async def exception_response(exception: CustomException) -> JSONResponse:
    return JSONResponse(
        content={
            "ok": False,
            "message": exception.message,
        },
        status_code=exception.status_code,
    )


async def server_exception_response() -> JSONResponse:
    return JSONResponse(
        content={
            "ok": False,
            "message": "Something went wrong. Please try again.",
        },
        status_code=500,
    )
