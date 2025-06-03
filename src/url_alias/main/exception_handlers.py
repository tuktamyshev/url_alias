import logging

from fastapi import FastAPI

from url_alias.controllers.http.v1.common.exc_handlers import map_exc_handlers

logger = logging.getLogger("webserver")


def setup_exc_handlers(app: FastAPI) -> None:
    map_exc_handlers(app)
