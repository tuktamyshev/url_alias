from dataclasses import dataclass
from uuid import UUID

from url_alias.domain.common.exceptions import AccessException


@dataclass(frozen=True)
class AccessService:
    def check_is_owner(self, user_uuid: UUID, owner_uuid: UUID) -> None:
        if owner_uuid == user_uuid:
            return
        raise AccessException
