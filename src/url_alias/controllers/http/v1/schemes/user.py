from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReadUserDTO(BaseModel):
    username: str
    uuid: UUID
    created_at: datetime
