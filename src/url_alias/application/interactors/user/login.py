from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel

from url_alias.application.common.base_interactor import Interactor
from url_alias.application.common.exceptions.auth import WrongUsernameOrPasswordException
from url_alias.application.interfaces.password_hasher import PasswordHasherInterface
from url_alias.application.interfaces.repositories.user import UserRepository


class UserLoginDTO(BaseModel):
    username: str
    password: str


@dataclass(frozen=True)
class LoginUserInteractor(Interactor[UserLoginDTO, UUID]):
    user_repository: UserRepository
    password_hasher_service: PasswordHasherInterface

    async def __call__(self, data: UserLoginDTO) -> UUID:
        if not (user := await self.user_repository.get_one_or_none(username=data.username)):
            raise WrongUsernameOrPasswordException()

        if not self.password_hasher_service.validate_password(
            password=data.password,
            hashed_password=user.hashed_password,
        ):
            raise WrongUsernameOrPasswordException()

        return user.uuid
