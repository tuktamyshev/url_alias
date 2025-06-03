from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.interfaces.alias_service import AliasServiceInterface
from url_alias.application.interfaces.repositories.url import URLRepository
from url_alias.application.interfaces.transaction_manager import TransactionManager
from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface
from url_alias.domain.entities.url import URLEntity


class CreateURLDTO(BaseModel):
    expires_in_days: int
    original_url: str


@dataclass(frozen=True)
class CreateURLInteractor(Interactor[CreateURLDTO, URLEntity]):
    transaction_manager: TransactionManager
    url_repository: URLRepository
    user_uuid_provider: UUIDProviderInterface
    alias_service: AliasServiceInterface

    async def __call__(self, data: CreateURLDTO) -> URLEntity:
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        alias = await self.alias_service.generate_unique_alias()
        url_entity = URLEntity.create(
            original_url=data.original_url,
            alias=alias,
            expires_at=datetime.now(UTC) + timedelta(days=data.expires_in_days),
            user_uuid=user_uuid,
        )
        async with self.transaction_manager:
            await self.url_repository.add(url_entity)

        return url_entity
