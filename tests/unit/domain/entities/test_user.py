from uuid import UUID

from url_alias.domain.entities.user import UserEntity


def test_user_create_success() -> None:
    username = "user"
    hashed_password = "hashed_pwd"

    user = UserEntity.create(username=username, hashed_password=hashed_password)

    assert isinstance(user.uuid, UUID)
    assert user.username == username
    assert user.hashed_password == hashed_password
    assert user.created_at is not None
