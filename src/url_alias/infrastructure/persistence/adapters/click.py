from dataclasses import dataclass

from url_alias.application.interfaces.repositories.click import ClickRepository
from url_alias.domain.entities.click import ClickEntity
from url_alias.infrastructure.persistence.adapters.base import SQLAlchemyRepository


@dataclass(frozen=True)
class SQLAlchemyClickRepository(ClickRepository, SQLAlchemyRepository):
    entity: ClickEntity = ClickEntity
