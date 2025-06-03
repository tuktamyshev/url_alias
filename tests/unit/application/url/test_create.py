from unittest.mock import AsyncMock, MagicMock, patch

from tests.factories.entities import URLEntityFactory, UserEntityFactory
from url_alias.application.interactors.url.create import CreateURLDTO, CreateURLInteractor
from url_alias.domain.entities.url import URLEntity


class TestCreateURLInteractor:
    def setup_method(self) -> None:
        self.url_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.transaction_manager = AsyncMock()
        self.alias_service = AsyncMock()
        self.user = UserEntityFactory()
        self.user_uuid_provider.get_current_user_uuid.return_value = self.user.uuid
        self.interactor = CreateURLInteractor(
            transaction_manager=self.transaction_manager,
            url_repository=self.url_repository,
            user_uuid_provider=self.user_uuid_provider,
            alias_service=self.alias_service,
        )

    async def test_create_url_success(self) -> None:
        url_entity = URLEntityFactory(user_uuid=self.user.uuid)
        self.alias_service.generate_unique_alias.return_value = url_entity.alias
        dto = CreateURLDTO(expires_in_days=1, original_url=url_entity.original_url)
        with patch("url_alias.application.interactors.url.create.URLEntity.create", return_value=url_entity):
            result = await self.interactor(dto)

        assert isinstance(result, URLEntity)
        assert result.original_url == url_entity.original_url
        assert result.alias == url_entity.alias
        assert result.user_uuid == self.user.uuid
        self.url_repository.add.assert_awaited_once_with(url_entity)
        self.alias_service.generate_unique_alias.assert_called_once_with()
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()
