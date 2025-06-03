from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.factories.entities import UserEntityFactory
from url_alias.application.common.exceptions.auth import WrongUsernameOrPasswordException
from url_alias.application.interactors.user.login import LoginUserInteractor, UserLoginDTO


class TestLoginUserInteractor:
    def setup_method(self) -> None:
        self.user_repository = AsyncMock()
        self.password_hasher_service = MagicMock()
        self.interactor = LoginUserInteractor(
            user_repository=self.user_repository,
            password_hasher_service=self.password_hasher_service,
        )

    async def test_login_success(self) -> None:
        user = UserEntityFactory()
        password = "password123"
        self.user_repository.get_one_or_none.return_value = user
        self.password_hasher_service.validate_password.return_value = True

        dto = UserLoginDTO(username=user.username, password=password)
        result = await self.interactor(dto)

        assert result == user.uuid
        self.user_repository.get_one_or_none.assert_awaited_once_with(username=user.username)
        self.password_hasher_service.validate_password.assert_called_once_with(
            password=password,
            hashed_password=user.hashed_password,
        )

    async def test_login_wrong_credentials(self) -> None:
        username = "user"
        password = "wrong_password"
        self.user_repository.get_one_or_none.return_value = None

        dto = UserLoginDTO(username=username, password=password)

        with pytest.raises(WrongUsernameOrPasswordException):
            await self.interactor(dto)
