from dataclasses import dataclass

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from url_alias.application.common.exceptions.user import UserWithThisUsernameAlreadyExistsException
from url_alias.application.interfaces.repositories.user import UserRepository
from url_alias.domain.entities.user import UserEntity
from url_alias.infrastructure.persistence.adapters.base import SQLAlchemyRepository


@dataclass(frozen=True)
class SQLAlchemyUserRepository(UserRepository, SQLAlchemyRepository):
    entity: UserEntity = UserEntity

    async def add(self, entity: UserEntity) -> None:
        try:
            return await super().add(entity)
        except IntegrityError as e:
            error_message = str(e.orig)
            if UniqueViolationError.__name__ in error_message and "username" in error_message:
                raise UserWithThisUsernameAlreadyExistsException(username=entity.username)
            raise e
