from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from url_alias.application.common.filter import PaginatedRequestDTO, PaginatedResponseDTO, SortOrder, URLSort
from url_alias.application.interfaces.repositories.base import BaseRepository
from url_alias.domain.entities.url import URLEntity


class URLInfoDTO(BaseModel):
    uuid: UUID
    user_uuid: UUID
    original_url: str
    alias: str
    alias_url: str
    is_active: bool
    expires_at: datetime
    created_at: datetime
    clicks_count: int


class URLListDTO(PaginatedResponseDTO[URLInfoDTO]):
    pass


class GetURLListDTO(PaginatedRequestDTO):
    is_active: bool | None
    sort_by: URLSort
    order: SortOrder


@dataclass(frozen=True)
class URLRepository(BaseRepository[URLEntity], ABC):
    def get_own_list(self, user_uuid: UUID, filters: GetURLListDTO) -> URLListDTO: ...

    async def increment_click_counter(self, uuid: UUID) -> None: ...
