from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.factories.entities import URLEntityFactory, UserEntityFactory
from url_alias.application.interactors.url.deactivate import DeactivateURLInteractor
from url_alias.domain.common.exceptions import AccessException


class TestDeactivateInteractor:
    def setup_method(self) -> None:
        self.url_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.access_service = MagicMock()
        self.transaction_manager = AsyncMock()
        self.user = UserEntityFactory()
        self.url = URLEntityFactory(user_uuid=self.user.uuid)
        self.user_uuid_provider.get_current_user_uuid.return_value = self.user.uuid
        self.interactor = DeactivateURLInteractor(
            transaction_manager=self.transaction_manager,
            url_repository=self.url_repository,
            user_uuid_provider=self.user_uuid_provider,
            access_service=self.access_service,
        )

    async def test_deactivate_success(self) -> None:
        self.url_repository.get_one_or_none.return_value = self.url
        await self.interactor(self.url.uuid)

        self.url_repository.get_one_or_none.assert_awaited_once_with(uuid=self.url.uuid)
        self.access_service.check_is_owner.assert_called_once_with(self.user.uuid, self.url)
        self.url_repository.update.assert_awaited_once_with(self.url.uuid, is_active=False)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_deactivate_not_owner(self) -> None:
        other_user = UserEntityFactory()
        self.user_uuid_provider.get_current_user_uuid.return_value = other_user.uuid
        self.access_service.check_is_owner.side_effect = AccessException()
        self.url_repository.get_one_or_none.return_value = self.url

        with pytest.raises(AccessException):
            await self.interactor(self.url.uuid)

        self.url_repository.get_one_or_none.assert_awaited_once_with(uuid=self.url.uuid)
        self.access_service.check_is_owner.assert_called_once_with(other_user.uuid, self.url)
        self.url_repository.update.assert_not_awaited()
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()
