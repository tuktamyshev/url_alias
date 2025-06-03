from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class BaseEntity:
    uuid: UUID
    created_at: datetime

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.uuid == other.uuid
