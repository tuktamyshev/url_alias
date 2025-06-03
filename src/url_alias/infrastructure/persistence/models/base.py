import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.orm import registry

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)

mapper_registry = registry(metadata=metadata)


def base_columns() -> list[sa.Column]:
    return [
        sa.Column("uuid", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    ]
