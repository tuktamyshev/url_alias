from abc import ABC, abstractmethod
from uuid import UUID


class UUIDProviderInterface(ABC):
    @abstractmethod
    def get_current_user_uuid(self) -> UUID: ...
