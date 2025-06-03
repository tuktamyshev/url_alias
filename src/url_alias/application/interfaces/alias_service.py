from abc import ABC, abstractmethod


class AliasServiceInterface(ABC):
    @abstractmethod
    async def generate_unique_alias(self) -> str: ...
