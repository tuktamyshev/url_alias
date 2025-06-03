from dataclasses import dataclass
from uuid import UUID

from url_alias.application.common.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class URLInactiveException(ApplicationException):
    uuid: UUID

    @property
    def message(self) -> str:
        return f"URL inactive: {self.uuid}"
