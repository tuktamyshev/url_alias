import logging
from functools import partial
from typing import TYPE_CHECKING, ClassVar, cast

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status as code
from starlette.requests import Request

from url_alias.application.common.exceptions.auth import AuthException
from url_alias.application.common.exceptions.base import ApplicationException
from url_alias.application.common.exceptions.repository import EntityNotFoundException
from url_alias.domain.common.exceptions import DomainException, FieldException

logger = logging.getLogger("webserver")

if TYPE_CHECKING:

    class StubError(Exception):
        message: ClassVar[str]


async def handle_exc(
    _: "Request",
    exc: Exception,
    status: int,
) -> ORJSONResponse:
    exc = cast("StubError", exc)
    return ORJSONResponse(content={"detail": exc.message}, status_code=status)


async def internal_trouble(request: Request, exc: Exception) -> ORJSONResponse:
    logger.exception(f"{request.url}: {exc}")
    return ORJSONResponse(
        content={"detail": "Internal server error"},
        status_code=code.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def map_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        FieldException,
        partial(handle_exc, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        EntityNotFoundException,
        partial(handle_exc, status=code.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        AuthException,
        partial(handle_exc, status=code.HTTP_403_FORBIDDEN),
    )

    app.add_exception_handler(
        ApplicationException,
        partial(handle_exc, status=code.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        DomainException,
        partial(handle_exc, status=code.HTTP_400_BAD_REQUEST),
    )
    app.exception_handler(Exception)(internal_trouble)
