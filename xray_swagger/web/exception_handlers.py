from __future__ import annotations

import typing

from fastapi import FastAPI, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import UJSONResponse
from loguru import logger

if typing.TYPE_CHECKING:
    from fastapi import Request


def register_exception_handlers(
    app: FastAPI,
) -> None:  # pragma: no cover
    """
    Actions to run on application's exeption handlers.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.exception_handler(ResponseValidationError)
    async def _response_model_validation_failed_handler(
        _: Request,
        exc: ResponseValidationError,
    ):
        validation_errors = exc.errors()
        logger.error(validation_errors)
        return UJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=validation_errors,
        )
