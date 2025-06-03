import pytest

from tests.factories.entities import URLEntityFactory, UserEntityFactory
from url_alias.domain.common.exceptions import AccessException
from url_alias.domain.services.access import AccessService


def test_check_is_owner_allows_owner(access_service: AccessService) -> None:
    user = UserEntityFactory()
    url_entity = URLEntityFactory(user_uuid=user.uuid)

    access_service.check_is_owner(user.uuid, url_entity.user_uuid)


def test_check_is_owner_denies_non_owner(access_service: AccessService) -> None:
    user = UserEntityFactory()
    url_entity = URLEntityFactory()
    with pytest.raises(AccessException):
        access_service.check_is_owner(user.uuid, url_entity.user_uuid)
