import pytest

from url_alias.domain.services.access import AccessService


@pytest.fixture(scope="session")
async def access_service() -> AccessService:
    return AccessService()
