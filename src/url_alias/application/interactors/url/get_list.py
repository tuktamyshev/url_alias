from dataclasses import dataclass

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.interfaces.repositories.url import GetURLListDTO, URLListDTO, URLRepository
from url_alias.application.interfaces.user_uuid_provider import UUIDProviderInterface


@dataclass(frozen=True)
class GetOwnURLListInteractor(Interactor[GetURLListDTO, URLListDTO]):
    repository: URLRepository
    user_uuid_provider: UUIDProviderInterface

    async def __call__(self, data: GetURLListDTO) -> URLListDTO:
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        urls = await self.repository.get_own_list(user_uuid, data)
        return urls
