import base64
import uuid
from dataclasses import dataclass

from url_alias.application.interfaces.alias_service import AliasServiceInterface
from url_alias.application.interfaces.repositories.url import URLRepository
from url_alias.infrastructure.config.asgi import ASGIConfig


@dataclass(frozen=True)
class AliasService(AliasServiceInterface):
    asgi_config: ASGIConfig
    url_repository: URLRepository

    async def generate_unique_alias(self) -> str:
        while True:
            uid = uuid.uuid4()
            alias = base64.urlsafe_b64encode(uid.bytes).decode("utf-8")[:8]
            if await self.url_repository.get_one_or_none(alias=alias) is None:
                return alias
