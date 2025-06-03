from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.factories.entities import UserEntityFactory
from url_alias.application.common.exceptions.user import UserWithThisUsernameAlreadyExistsException
from url_alias.application.interactors.user.register import RegisterUserInteractor, UserCreateDTO
from url_alias.domain.entities.user import UserEntity


class TestRegisterUserInteractor:
    def setup_method(self) -> None:
        self.user_repository = AsyncMock()
        self.transaction_manager = AsyncMock()
        self.email_service = AsyncMock()
        self.password_hasher_service = MagicMock()
        self.interactor = RegisterUserInteractor(
            user_repository=self.user_repository,
            transaction_manager=self.transaction_manager,
            password_hasher_service=self.password_hasher_service,
        )

    async def test_register_user_success(self) -> None:
        username = "username"
        password = "password123"
        hashed_password = "hashed_password"
        self.password_hasher_service.hash_password.return_value = hashed_password
        self.user_repository.get_one_or_none.return_value = None

        dto = UserCreateDTO(username=username, password=password)
        result = await self.interactor(dto)

        assert isinstance(result, UserEntity)
        assert result.username == username
        assert result.hashed_password == hashed_password
        self.password_hasher_service.hash_password.assert_called_once_with(password)
        self.user_repository.add.assert_awaited_once()
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_register_user_already_exists(self) -> None:
        username = "username"
        password = "password123"
        existing_user = UserEntityFactory()
        self.user_repository.get_one_or_none.return_value = existing_user
        self.user_repository.add.side_effect = UserWithThisUsernameAlreadyExistsException(username)

        dto = UserCreateDTO(username=username, password=password)

        with pytest.raises(UserWithThisUsernameAlreadyExistsException):
            await self.interactor(dto)

        self.user_repository.add.assert_awaited_once()
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()
