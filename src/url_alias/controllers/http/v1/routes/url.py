from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette import status
from starlette.responses import RedirectResponse

from url_alias.application.interactors.url.create import CreateURLDTO, CreateURLInteractor
from url_alias.application.interactors.url.deactivate import DeactivateURLInteractor
from url_alias.application.interactors.url.get_list import GetOwnURLListInteractor
from url_alias.application.interactors.url.redirect import RedirectInteractor
from url_alias.application.interfaces.repositories.url import GetURLListDTO, URLListDTO
from url_alias.controllers.http.v1.common.schemes import CreateURLSchema
from url_alias.controllers.http.v1.schemes.url import ReadURLDTO, URLFilter
from url_alias.infrastructure.config.asgi import ASGIConfig

router = APIRouter(
    prefix="/url",
    tags=["url"],
    route_class=DishkaRoute,
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(
    data: CreateURLSchema,
    interactor: FromDishka[CreateURLInteractor],
    asgi_config: FromDishka[ASGIConfig],
) -> ReadURLDTO:
    url_entity = await interactor(
        CreateURLDTO(
            expires_in_days=data.expires_in_days,
            original_url=str(data.original_url),
        )
    )
    return ReadURLDTO(
        **asdict(url_entity),
        alias_url=f"{asgi_config.BACKEND_URL}/api/v1/url/{url_entity.alias}",
    )


@router.patch("/deactivate")
async def deactivate(
    uuid: UUID,
    interactor: FromDishka[DeactivateURLInteractor],
) -> None:
    await interactor(uuid)


@router.get("/own_list")
async def own_list(
    filters: Annotated[URLFilter, Query()],
    interactor: FromDishka[GetOwnURLListInteractor],
) -> URLListDTO:
    return await interactor(GetURLListDTO(**filters.model_dump()))


@router.get("/{alias}")
async def redirect_to_original(
    alias: str,
    interactor: FromDishka[RedirectInteractor],
) -> RedirectResponse:
    original_url = await interactor(alias)
    # Swagger does not redirect automatic
    return RedirectResponse(original_url)
