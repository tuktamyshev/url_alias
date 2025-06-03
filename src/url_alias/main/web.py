from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from url_alias.infrastructure.config.main_config import Config
from url_alias.infrastructure.logging import setup_logging
from url_alias.main.api_gateway import setup_routers
from url_alias.main.di.setup import setup_web_di
from url_alias.main.exception_handlers import setup_exc_handlers
from url_alias.main.map_tables import setup_map_tables
from url_alias.main.middlewares import setup_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    yield

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    config = Config()
    app = FastAPI(
        default_response_class=ORJSONResponse,
        title="URL alias",
        version="1.0.0",
        docs_url="/docs",
        description="URL alias",
        lifespan=lifespan,
        debug=config.asgi.FASTAPI_DEBUG,
        root_path="/api",
    )
    app.state.config = config

    setup_middlewares(app)
    setup_web_di(app)
    setup_routers(app)
    setup_map_tables()
    setup_exc_handlers(app)
    setup_logging()

    return app
