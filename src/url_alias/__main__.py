import uvicorn

from url_alias.infrastructure.config.main_config import Config
from url_alias.infrastructure.logging import setup_logging

if __name__ == "__main__":
    asgi_config = Config().asgi
    logging_config = setup_logging()

    uvicorn.run(
        app="url_alias.main.web:create_app",
        port=asgi_config.UVICORN_PORT,
        host="0.0.0.0",  # nosec
        factory=True,
        reload=True,
        log_config=logging_config,
    )
