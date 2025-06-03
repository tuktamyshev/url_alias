from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Interactor[InputDTO, OutputDTO](ABC):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO: ...
