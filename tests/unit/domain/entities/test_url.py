from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from url_alias.domain.entities.url import URLEntity


def test_url_create_success() -> None:
    user_uuid = uuid4()
    original_url = "url"
    alias = "alias"
    expires_at = datetime.now(UTC) + timedelta(days=1)

    url = URLEntity.create(user_uuid=user_uuid, original_url=original_url, alias=alias, expires_at=expires_at)

    assert isinstance(url.uuid, UUID)
    assert url.user_uuid == user_uuid
    assert url.original_url == original_url
    assert url.alias == alias
    assert url.expires_at == expires_at
    assert url.created_at is not None
