from dishka import Provider, provide
from fastapi.security import APIKeyCookie

from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.config.auth import AuthConfig
from url_alias.infrastructure.cookie_service import CookieService


class CookieServiceProvider(Provider):
    @provide
    def cookie_service(self, app_config: ASGIConfig, auth_config: AuthConfig) -> CookieService:
        return CookieService(
            access_token_cookie_scheme=APIKeyCookie(name="access_token"),
            refresh_token_cookie_scheme=APIKeyCookie(name="refresh_token"),
            app_config=app_config,
            auth_config=auth_config,
        )
