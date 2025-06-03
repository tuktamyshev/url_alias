from abc import ABC
from dataclasses import dataclass

from url_alias.application.interfaces.repositories.base import BaseRepository
from url_alias.domain.entities.user import UserEntity


@dataclass(frozen=True)
class UserRepository(BaseRepository[UserEntity], ABC): ...
