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
    created_at = "created_at"
    clicks_count = "clicks_count"
    alias = "alias"
