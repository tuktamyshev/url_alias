from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta

from sqlalchemy import asc, desc, func, select

from url_alias.application.common.filter import SortOrder, URLSort
from url_alias.application.interfaces.repositories.url import (
    GetURLListDTO,
    URLInfoDTO,
    URLListDTO,
    URLRepository,
)
from url_alias.domain.common.base_entity import BaseEntity
from url_alias.domain.entities.click import ClickEntity
from url_alias.domain.entities.url import UUID, URLEntity
from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.persistence.adapters.base import SQLAlchemyRepository


@dataclass(frozen=True)
class SQLAlchemyURLRepository(URLRepository, SQLAlchemyRepository[URLEntity]):
    asgi_config: ASGIConfig = field(kw_only=True)
    entity: BaseEntity = URLEntity

    async def get_own_list(self, user_uuid: UUID, filters: GetURLListDTO) -> URLListDTO:
        now = datetime.now(UTC)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        sub_last_hour = (
            select(ClickEntity.url_uuid, func.count().label("last_hour_clicks"))
            .where(ClickEntity.created_at >= hour_ago)
            .group_by(ClickEntity.url_uuid)
            .subquery()
        )

        sub_last_day = (
            select(ClickEntity.url_uuid, func.count().label("last_day_clicks"))
            .where(ClickEntity.created_at >= day_ago)
            .group_by(ClickEntity.url_uuid)
            .subquery()
        )

        sort_fields_map = {
            URLSort.alias: URLEntity.alias,
            URLSort.created_at: URLEntity.created_at,
            URLSort.last_hour_clicks: func.coalesce(sub_last_hour.c.last_hour_clicks, 0).label("last_hour_clicks"),
            URLSort.last_day_clicks: func.coalesce(sub_last_day.c.last_day_clicks, 0).label("last_day_clicks"),
        }

        sort_column = sort_fields_map[filters.sort_by]
        ordering = asc(sort_column) if filters.order == SortOrder.ASC else desc(sort_column)

        query = (
            select(
                URLEntity,
                func.count().over().label("total_count"),
                func.coalesce(sub_last_hour.c.last_hour_clicks, 0),
                func.coalesce(sub_last_day.c.last_day_clicks, 0),
            )
            .filter_by(user_uuid=user_uuid)
            .limit(filters.limit)
            .offset(filters.offset)
            .order_by(ordering)
            .outerjoin(sub_last_hour, URLEntity.uuid == sub_last_hour.c.url_uuid)
            .outerjoin(sub_last_day, URLEntity.uuid == sub_last_day.c.url_uuid)
        )

        if filters.is_active is not None:
            query = query.where(URLEntity.is_active == filters.is_active)

        result = await self.session.execute(query)

        rows = result.all()

        url_list = []
        total_count = 0
        for (
            url,
            count,
            last_hour_clicks,
            last_day_clicks,
        ) in rows:
            url_list.append(
                URLInfoDTO(
                    **asdict(url),
                    alias_url=f"{self.asgi_config.BACKEND_URL}/v1/url/{url.alias}",
                    last_hour_clicks=last_hour_clicks,
                    last_day_clicks=last_day_clicks,
                )
            )
            total_count = count

        return URLListDTO(items=url_list, total=total_count)
