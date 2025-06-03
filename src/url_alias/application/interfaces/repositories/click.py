from abc import ABC
from dataclasses import dataclass

from url_alias.application.interfaces.repositories.base import BaseRepository
from url_alias.domain.entities.click import ClickEntity


@dataclass(frozen=True)
class ClickRepository(BaseRepository[ClickEntity], ABC): ...
