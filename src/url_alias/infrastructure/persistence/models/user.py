import sqlalchemy as sa

from url_alias.domain.entities.user import UserEntity
from url_alias.infrastructure.persistence.models.base import base_columns, mapper_registry

user_table = sa.Table(
    "user",
    mapper_registry.metadata,
    *base_columns(),
    sa.Column("username", sa.String(320), nullable=False, unique=True, index=True),
    sa.Column("hashed_password", sa.String(1024), nullable=False),
)


def map_user_table() -> None:
    _ = mapper_registry.map_imperatively(
        UserEntity,
        user_table,
        properties={
            "uuid": user_table.c.uuid,
            "created_at": user_table.c.created_at,
            "username": user_table.c.username,
            "hashed_password": user_table.c.hashed_password,
        },
    )
