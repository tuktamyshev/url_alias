import sqlalchemy as sa

from url_alias.domain.entities.url import URLEntity
from url_alias.infrastructure.persistence.models.base import base_columns, mapper_registry

url_table = sa.Table(
    "url",
    mapper_registry.metadata,
    *base_columns(),
    sa.Column(
        "user_uuid",
        sa.UUID,
        sa.ForeignKey("user.uuid", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("original_url", sa.String(1024), nullable=False),
    sa.Column("alias", sa.String(1024), nullable=False, unique=True),
    sa.Column("is_active", sa.Boolean, nullable=False),
    sa.Column(
        "expires_at",
        sa.DateTime(timezone=True),
        nullable=False,
    ),
    sa.Column("clicks_count", sa.Integer, nullable=False),
)


def map_url_table() -> None:
    _ = mapper_registry.map_imperatively(
        URLEntity,
        url_table,
        properties={
            "uuid": url_table.c.uuid,
            "created_at": url_table.c.created_at,
            "original_url": url_table.c.original_url,
            "alias": url_table.c.alias,
            "is_active": url_table.c.is_active,
            "expires_at": url_table.c.expires_at,
            "clicks_count": url_table.c.clicks_count,
        },
    )
