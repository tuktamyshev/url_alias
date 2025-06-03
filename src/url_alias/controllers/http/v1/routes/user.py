from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from url_alias.application.interfaces.repositories.user import UserRepository
from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface
from url_alias.controllers.http.v1.schemes.user import ReadUserDTO
from url_alias.domain.entities.user import UserEntity

router = APIRouter(
    prefix="/user",
    tags=["user"],
    route_class=DishkaRoute,
)


@router.get("/me", response_model=ReadUserDTO)
async def me(
    user_uuid_provider: FromDishka[UUIDProviderInterface],
    user_repository: FromDishka[UserRepository],
) -> UserEntity:
    user_uuid = user_uuid_provider.get_current_user_uuid()
    return await user_repository.get_one_or_none(uuid=user_uuid)
