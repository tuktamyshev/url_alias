from dishka import Provider, provide

from url_alias.infrastructure.auth import JWTTokenService


class JWTAuthServiceProvider(Provider):
    auth_service = provide(JWTTokenService)
