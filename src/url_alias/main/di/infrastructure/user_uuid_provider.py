from dishka import Provider, Scope, provide
from starlette.requests import Request

from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface
from url_alias.infrastructure.config.auth import AuthConfig
from url_alias.infrastructure.constants import JWTTokenType
from url_alias.infrastructure.cookie_service import CookieService
from url_alias.infrastructure.user_uuid_provider import AuthByTokenDTO, TokenUUIDProvider


class TokenUUIDProviderProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def user_uuid_provider(
        self,
        cookie_service: CookieService,
        auth_config: AuthConfig,
        request: Request,
    ) -> UUIDProviderInterface:
        cookie_scheme = cookie_service.access_token_cookie_scheme
        token = await cookie_scheme(request)

        return TokenUUIDProvider(
            token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.ACCESS.value),
            auth_config=auth_config,
        )
