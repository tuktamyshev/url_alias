from dataclasses import dataclass
from datetime import UTC, datetime

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.common.exceptions.repository import EntityNotFoundException
from url_alias.application.common.exceptions.url import URLInactiveException
from url_alias.application.interfaces.repositories.click import ClickRepository
from url_alias.application.interfaces.repositories.url import URLRepository
from url_alias.application.interfaces.transaction_manager import TransactionManager
from url_alias.domain.entities.click import ClickEntity


@dataclass(frozen=True)
class RedirectInteractor(Interactor[str, str]):
    transaction_manager: TransactionManager
    click_repository: ClickRepository
    url_repository: URLRepository

    async def __call__(self, data: str) -> str:
        alias = data
        url_entity = await self.url_repository.get_one_or_none(alias=alias)
        if not url_entity:
            raise EntityNotFoundException()

        if not url_entity.is_active or datetime.now(UTC) > url_entity.expires_at:
            raise URLInactiveException(uuid=url_entity.uuid)

        click = ClickEntity.create(url_uuid=url_entity.uuid)
        async with self.transaction_manager:
            await self.click_repository.add(click)

        return url_entity.original_url
