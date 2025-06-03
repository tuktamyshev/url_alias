from datetime import UTC, datetime, timedelta
from uuid import uuid4

import bcrypt
import factory
from faker import Faker

from url_alias.domain.entities.click import ClickEntity
from url_alias.domain.entities.url import URLEntity
from url_alias.domain.entities.user import UserEntity

fake = Faker()


class URLEntityFactory(factory.Factory):
    class Meta:
        model = URLEntity

    uuid = factory.LazyFunction(uuid4)
    user_uuid = factory.LazyFunction(uuid4)
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
    original_url = factory.LazyFunction(fake.url)
    alias = factory.LazyFunction(fake.word)
    is_active = factory.LazyFunction(fake.boolean)
    expires_at = factory.LazyFunction(lambda: datetime.now(UTC) + timedelta(hours=1))


class UserEntityFactory(factory.Factory):
    class Meta:
        model = UserEntity

    uuid = factory.LazyFunction(uuid4)
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
    username = factory.LazyFunction(fake.word)
    hashed_password = factory.LazyFunction(fake.word)

    @factory.post_generation
    def password(self, _create: bool, extracted: str | None) -> None:
        pwd = extracted or "password"

        salt = bcrypt.gensalt()
        pwd_bytes = pwd.encode("utf-8")
        self.hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

class ClickEntityFactory(factory.Factory):
    class Meta:
        model = ClickEntity

    uuid = factory.LazyFunction(uuid4)
    url_uuid = factory.LazyFunction(uuid4)
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
