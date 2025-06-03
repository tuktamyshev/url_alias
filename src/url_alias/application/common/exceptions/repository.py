from dataclasses import dataclass

from url_alias.application.common.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class EntityNotFoundException(ApplicationException):
    @property
    def message(self) -> str:
        return "Entity not found"
