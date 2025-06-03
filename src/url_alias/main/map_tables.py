from url_alias.infrastructure.persistence.models.url import map_url_table
from url_alias.infrastructure.persistence.models.user import map_user_table


def setup_map_tables() -> None:
    map_user_table()
    map_url_table()
