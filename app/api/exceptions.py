from logging import Logger

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def add_exceptions(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    @app.exception_handler(Exception)
    async def exception_logger_handler(
        request: Request,
        exc: Exception,
    ):
        logger: Logger = await request.app.state.dishka_container.get(Logger)
        logger.exception(str(exc))
        raise exc
