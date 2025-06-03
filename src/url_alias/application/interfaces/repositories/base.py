from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class BaseRepository[ET](ABC):
    @abstractmethod
    async def add(self, entity: ET) -> ET: ...

    @abstractmethod
    async def get_one_or_none(self, **kwargs: Any) -> ET | None: ...

    @abstractmethod
    async def update(self, uuid: UUID, **kwargs: Any) -> ET: ...
