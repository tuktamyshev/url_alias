from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class DomainException(Exception):
    @property
    def message(self) -> str:
        return "DomainException occurred"


@dataclass(eq=False, frozen=True)
class FieldException(DomainException):
    @property
    def message(self) -> str:
        return "FieldException occurred"


@dataclass(eq=False, frozen=True)
class AccessException(DomainException):
    @property
    def message(self) -> str:
        return "Access denied"
