from dishka import Provider, provide

from url_alias.application.interfaces.password_hasher import PasswordHasherInterface
from url_alias.infrastructure.password_hasher import PasswordHasherService


class PasswordHasherProvider(Provider):
    password_hasher = provide(PasswordHasherService, provides=PasswordHasherInterface)
