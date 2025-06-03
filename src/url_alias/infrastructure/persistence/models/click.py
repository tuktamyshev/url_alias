import sqlalchemy as sa

from url_alias.domain.entities.click import ClickEntity
from url_alias.infrastructure.persistence.models.base import base_columns, mapper_registry

click_table = sa.Table(
    "click",
    mapper_registry.metadata,
    *base_columns(),
    sa.Column(
        "url_uuid",
        sa.UUID,
        sa.ForeignKey("url.uuid", ondelete="CASCADE"),
        nullable=False,
    ),
)


def map_click_table() -> None:
    _ = mapper_registry.map_imperatively(
        ClickEntity,
        click_table,
        properties={
            "uuid": click_table.c.uuid,
            "created_at": click_table.c.created_at,
            "url_uuid": click_table.c.url_uuid,
        },
    )
