from dataclasses import dataclass

from url_alias.application.common.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class UserWithThisUsernameAlreadyExistsException(ApplicationException):
    username: str

    @property
    def message(self) -> str:
        return f"User with this username already exists: {self.username}"
