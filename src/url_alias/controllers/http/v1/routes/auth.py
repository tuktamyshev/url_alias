from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute, inject
from fastapi import APIRouter, Depends, Form
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from url_alias.application.interactors.user.login import LoginUserInteractor, UserLoginDTO
from url_alias.application.interactors.user.register import RegisterUserInteractor, UserCreateDTO
from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface
from url_alias.controllers.http.v1.schemes.user import ReadUserDTO
from url_alias.domain.entities.user import UserEntity
from url_alias.infrastructure.auth import JWTTokenService
from url_alias.infrastructure.config.auth import AuthConfig
from url_alias.infrastructure.constants import JWTTokenType
from url_alias.infrastructure.cookie_service import CookieService
from url_alias.infrastructure.user_uuid_provider import AuthByTokenDTO, TokenUUIDProvider

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadUserDTO,
)
async def register(
    interactor: FromDishka[RegisterUserInteractor],
    username: str = Form(),
    password: str = Form(),
) -> UserEntity:
    user_data = UserCreateDTO(username=username, password=password)
    user = await interactor(user_data)
    return user


@router.post("/login")
async def login(
    response: Response,
    login_interactor: FromDishka[LoginUserInteractor],
    cookie_service: FromDishka[CookieService],
    token_service: FromDishka[JWTTokenService],
    username: str = Form(),
    password: str = Form(),
) -> None:
    data = UserLoginDTO(username=username, password=password)
    user_uuid = await login_interactor(data)

    tokens_info = token_service.create_tokens(user_uuid)
    cookie_service.set_access_token_cookie(
        response,
        access_token=tokens_info.access_token,
    )
    cookie_service.set_refresh_token_cookie(
        response,
        refresh_token=tokens_info.refresh_token,
    )


@router.post("/logout")
async def logout(
    response: Response,
    uuid_provider: FromDishka[UUIDProviderInterface],
    cookie_service: FromDishka[CookieService],
) -> None:
    uuid_provider.get_current_user_uuid()
    cookie_service.delete_cookies(response)


@inject
async def get_user_uuid_provider_from_refresh_token(
    request: Request,
    cookie_service: FromDishka[CookieService],
    auth_config: FromDishka[AuthConfig],
) -> UUIDProviderInterface:
    cookie_scheme = cookie_service.refresh_token_cookie_scheme
    token = await cookie_scheme(request)
    return TokenUUIDProvider(
        token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.REFRESH.value),
        auth_config=auth_config,
    )


@router.post("/refresh")
async def refresh(
    response: Response,
    token_service: FromDishka[JWTTokenService],
    cookie_service: FromDishka[CookieService],
    uuid_provider: UUIDProviderInterface = Depends(get_user_uuid_provider_from_refresh_token),
) -> None:
    user_uuid = uuid_provider.get_current_user_uuid()
    access_token = token_service.create_access_token(user_uuid)
    cookie_service.set_access_token_cookie(
        response,
        access_token=access_token,
    )
