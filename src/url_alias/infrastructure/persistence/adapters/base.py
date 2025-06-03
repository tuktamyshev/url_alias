from abc import ABC
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from url_alias.application.interfaces.repositories.base import BaseRepository
from url_alias.domain.common.base_entity import BaseEntity


@dataclass(frozen=True)
class SQLAlchemyRepository[ET](BaseRepository, ABC):
    session: AsyncSession
    entity: type[BaseEntity]

    async def add(self, entity: BaseEntity) -> None:
        self.session.add(entity)
        await self.session.flush()

    async def get_one_or_none(self, **filters: Any) -> ET | None:
        query = select(self.entity).filter_by(**filters)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def update(self, uuid: UUID, **kwargs: Any) -> ET:
        entity = await self.session.get_one(self.entity, uuid)
        for attr, value in kwargs.items():
            setattr(entity, attr, value)
        await self.session.flush()
        return entity
