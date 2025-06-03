from dishka import Provider, Scope, from_context, provide

from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.config.auth import AuthConfig
from url_alias.infrastructure.config.db import DatabaseConfig
from url_alias.infrastructure.config.main_config import Config


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(Config)

    @provide
    def app_config(self, config: Config) -> ASGIConfig:
        return config.asgi

    @provide
    def auth_config(self, config: Config) -> AuthConfig:
        return config.auth

    @provide
    def db_config(self, config: Config) -> DatabaseConfig:
        return config.db
