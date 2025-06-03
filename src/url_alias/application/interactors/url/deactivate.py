from dataclasses import dataclass
from uuid import UUID

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.common.exceptions.repository import EntityNotFoundException
from url_alias.application.interfaces.repositories.url import URLRepository
from url_alias.application.interfaces.transaction_manager import TransactionManager
from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface
from url_alias.domain.services.access import AccessService


@dataclass(frozen=True)
class DeactivateURLInteractor(Interactor[UUID, None]):
    transaction_manager: TransactionManager
    url_repository: URLRepository
    user_uuid_provider: UUIDProviderInterface
    access_service: AccessService

    async def __call__(self, data: UUID) -> None:
        url_entity = await self.url_repository.get_one_or_none(uuid=data)
        if not url_entity:
            raise EntityNotFoundException()

        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        self.access_service.check_is_owner(user_uuid, url_entity.user_uuid)

        async with self.transaction_manager:
            await self.url_repository.update(url_entity.uuid, is_active=False)
