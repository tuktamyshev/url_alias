from dataclasses import dataclass

from url_alias.application.common.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class AuthException(ApplicationException):
    @property
    def message(self) -> str:
        return "Auth failed"


class WrongUsernameOrPasswordException(AuthException):
    @property
    def message(self) -> str:
        return "Wrong username or password"


class WrongTokenException(AuthException):
    @property
    def message(self) -> str:
        return "Wrong token"
