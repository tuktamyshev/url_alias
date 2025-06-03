from fastapi import APIRouter, FastAPI

from url_alias.controllers.http.v1.routes import auth, healthcheck, url, user


def setup_routers(app: FastAPI) -> None:
    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(healthcheck.router)
    router_v1.include_router(user.router)
    router_v1.include_router(auth.router)
    router_v1.include_router(url.router)

    app.include_router(router_v1)
