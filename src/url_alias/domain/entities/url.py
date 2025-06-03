from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from url_alias.domain.common.base_entity import BaseEntity


@dataclass
class URLEntity(BaseEntity):
    user_uuid: UUID
    original_url: str
    alias: str
    is_active: bool
    expires_at: datetime
    clicks_count: int

    @classmethod
    def create(cls, user_uuid: UUID, original_url: str, alias: str, expires_at: datetime) -> "URLEntity":
        return URLEntity(
            uuid=uuid4(),
            created_at=datetime.now(),
            user_uuid=user_uuid,
            original_url=original_url,
            alias=alias,
            is_active=True,
            expires_at=expires_at,
            clicks_count=0,
        )
