from enum import Enum

from pydantic import BaseModel


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class PaginatedRequestDTO(BaseModel):
    limit: int
    offset: int


class PaginatedResponseDTO[IT](BaseModel):
    total: int
    items: list[IT]


class URLSort(str, Enum):
    alias = "alias"
    created_at = "created_at"
    last_hour_clicks = "last_hour_clicks"
    last_day_clicks = "last_day_clicks"
