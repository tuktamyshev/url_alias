from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from url_alias.domain.common.base_entity import BaseEntity


@dataclass
class ClickEntity(BaseEntity):
    url_uuid: UUID

    @classmethod
    def create(cls, url_uuid: UUID) -> "ClickEntity":
        return ClickEntity(
            uuid=uuid4(),
            created_at=datetime.now(),
            url_uuid=url_uuid,
        )
