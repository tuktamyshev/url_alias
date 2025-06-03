from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from url_alias.domain.common.base_entity import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    username: str
    hashed_password: str

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "UserEntity":
        return cls(
            uuid=uuid4(),
            created_at=datetime.now(),
            username=username,
            hashed_password=hashed_password,
        )
