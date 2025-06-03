import logging
import logging.config
import os
from typing import Any

from url_alias.infrastructure.config import BASE_DIR

LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> dict[str, Any]:
    os.makedirs(LOG_DIR, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "json_indent": 2,
            },
            "console": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
        },
        "filters": {
            "webserver": {"()": "logging.Filter", "name": "webserver"},
            "url": {"()": "logging.Filter", "name": "url"},
            "user": {"()": "logging.Filter", "name": "user"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "webserver": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/webserver.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "json",
                "level": "DEBUG",
                "filters": ["webserver"],
            },
            "url": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/url.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "json",
                "level": "DEBUG",
                "filters": ["url"],
            },
            "user": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/user.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "json",
                "level": "DEBUG",
                "filters": ["user"],
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "webserver": {
                "level": "DEBUG",
                "handlers": ["webserver", "console"],
            },
            "url": {
                "level": "DEBUG",
                "handlers": ["url", "console"],
            },
            "user": {
                "level": "DEBUG",
                "handlers": ["user", "console"],
            },
        },
    }

    logging.config.dictConfig(logging_config)
    return logging_config
