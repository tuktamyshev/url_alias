from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.factories.entities import URLEntityFactory, UserEntityFactory, ClickEntityFactory
from url_alias.application.common.exceptions.url import URLInactiveException
from url_alias.application.interactors.url.redirect import RedirectInteractor
from url_alias.domain.entities.click import ClickEntity


class TestRedirectInteractor:
    def setup_method(self) -> None:
        self.url_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.transaction_manager = AsyncMock()
        self.click_repository = AsyncMock()
        self.user = UserEntityFactory()
        self.url = URLEntityFactory(user_uuid=self.user.uuid)
        self.click_entity = ClickEntityFactory(url_uuid=self.url.uuid)
        self.interactor = RedirectInteractor(
            transaction_manager=self.transaction_manager,
            url_repository=self.url_repository,
            click_repository=self.click_repository,
        )

    async def test_redirect_success(self) -> None:
        self.url.is_active = True
        self.url_repository.get_one_or_none.return_value = self.url

        with patch("url_alias.application.interactors.url.redirect.ClickEntity.create", return_value=self.click_entity) as mock_create:
            await self.interactor(self.url.alias)
            mock_create.assert_called_once_with(url_uuid=self.url.uuid)

        self.url_repository.get_one_or_none.assert_awaited_once()
        self.click_repository.add.assert_awaited_once_with(self.click_entity)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_redirect_inactive(self) -> None:
        self.url.is_active = False
        self.url_repository.get_one_or_none.return_value = self.url
        with pytest.raises(URLInactiveException):
            await self.interactor(self.url.alias)

        self.url_repository.get_one_or_none.assert_awaited_once_with(alias=self.url.alias)
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()

    async def test_redirect_expired(self) -> None:
        self.url.is_active = True
        self.url.expires_at = datetime.now(UTC)
        self.url_repository.get_one_or_none.return_value = self.url
        with pytest.raises(URLInactiveException):
            await self.interactor(self.url.alias)

        self.url_repository.get_one_or_none.assert_awaited_once_with(alias=self.url.alias)
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()
