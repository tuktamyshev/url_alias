from pydantic_settings import BaseSettings, SettingsConfigDict

from url_alias.infrastructure.config import BASE_DIR
from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.config.auth import AuthConfig
from url_alias.infrastructure.config.db import DatabaseConfig


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/env/.env",
        env_nested_delimiter="__",
    )

    asgi: ASGIConfig
    auth: AuthConfig
    db: DatabaseConfig
