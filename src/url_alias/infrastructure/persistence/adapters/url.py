from dataclasses import asdict, dataclass, field

from sqlalchemy import asc, desc, func, select, update

from url_alias.application.common.filter import SortOrder
from url_alias.application.interfaces.repositories.url import (
    GetURLListDTO,
    URLInfoDTO,
    URLListDTO,
    URLRepository,
)
from url_alias.domain.common.base_entity import BaseEntity
from url_alias.domain.entities.url import UUID, URLEntity
from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.persistence.adapters.base import SQLAlchemyRepository


@dataclass(frozen=True)
class SQLAlchemyURLRepository(URLRepository, SQLAlchemyRepository[URLEntity]):
    asgi_config: ASGIConfig = field(kw_only=True)
    entity: BaseEntity = URLEntity

    async def get_own_list(self, user_uuid: UUID, filters: GetURLListDTO) -> URLListDTO:
        sort_column = filters.sort_by
        ordering = asc(sort_column) if filters.order == SortOrder.ASC else desc(sort_column)

        query = (
            select(
                URLEntity,
                func.count().over().label("total_count"),
            )
            .filter_by(user_uuid=user_uuid)
            .limit(filters.limit)
            .offset(filters.offset)
            .order_by(ordering)
        )

        if filters.is_active:
            query = query.filter_by(is_active=filters.is_active)

        result = await self.session.execute(query)

        rows = result.all()

        url_list = []
        total_count = 0
        for (
            url,
            count,
        ) in rows:
            url_list.append(URLInfoDTO(**asdict(url), alias_url=f"{self.asgi_config.BACKEND_URL}/v1/url/{url.alias}"))
            total_count = count

        return URLListDTO(items=url_list, total=total_count)

    async def increment_click_counter(self, uuid: UUID) -> None:
        stmt = update(URLEntity).where(URLEntity.uuid == uuid).values(clicks_count=URLEntity.clicks_count + 1)
        await self.session.execute(stmt)
        await self.session.flush()
