import logging
from dataclasses import dataclass

from pydantic import BaseModel

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.interfaces.password_hasher import PasswordHasherInterface
from url_alias.application.interfaces.repositories.user import UserRepository
from url_alias.application.interfaces.transaction_manager import TransactionManager
from url_alias.domain.entities.user import UserEntity

logger = logging.getLogger("user")


class UserCreateDTO(BaseModel):
    username: str
    password: str


@dataclass(frozen=True)
class RegisterUserInteractor(Interactor[UserCreateDTO, UserEntity]):
    user_repository: UserRepository
    transaction_manager: TransactionManager
    password_hasher_service: PasswordHasherInterface

    async def __call__(self, data: UserCreateDTO) -> UserEntity:
        hashed_password = self.password_hasher_service.hash_password(data.password)

        user_entity = UserEntity.create(username=data.username, hashed_password=hashed_password)

        async with self.transaction_manager:
            await self.user_repository.add(user_entity)
        logger.debug(f"New user registered {data.username=}")

        return user_entity
