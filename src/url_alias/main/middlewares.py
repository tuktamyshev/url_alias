from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI) -> None:
    asgi_config = app.state.config.asgi
    app.add_middleware(
        CORSMiddleware,
        allow_origins=asgi_config.ALLOW_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
