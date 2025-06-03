from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from url_alias.application.common.filter import SortOrder, URLSort
from url_alias.controllers.http.v1.common.pagination import PaginationSchema


class ReadURLDTO(BaseModel):
    uuid: UUID
    user_uuid: UUID
    original_url: str
    alias: str
    alias_url: str
    is_active: bool
    expires_at: datetime
    created_at: datetime


class URLFilter(PaginationSchema):
    is_active: bool | None = Field(None)
    sort_by: URLSort = URLSort.created_at
    order: SortOrder = SortOrder.ASC
