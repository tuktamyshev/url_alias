from dishka import Scope

from url_alias.main.di.infrastructure.auth import JWTAuthServiceProvider
from url_alias.main.di.infrastructure.config import ConfigProvider
from url_alias.main.di.infrastructure.cookie_service import CookieServiceProvider
from url_alias.main.di.infrastructure.password_hasher import PasswordHasherProvider
from url_alias.main.di.infrastructure.persistence.database import SQLAlchemyDatabaseProvider
from url_alias.main.di.infrastructure.persistence.repositories import SQLAlchemyRepositoriesProvider
from url_alias.main.di.infrastructure.persistence.transaction_manager import SQLAlchemyTransactionManagerProvider
from url_alias.main.di.infrastructure.url_alias_service import ALiasServiceProvider
from url_alias.main.di.infrastructure.user_uuid_provider import TokenUUIDProviderProvider


class InfrastructureProvider(
    #  Not tied to business logic and do not implement interfaces
    CookieServiceProvider,
    JWTAuthServiceProvider,
    SQLAlchemyDatabaseProvider,
    ConfigProvider,
    # Realizations of interfaces
    SQLAlchemyTransactionManagerProvider,
    TokenUUIDProviderProvider,
    SQLAlchemyRepositoriesProvider,
    PasswordHasherProvider,
    ALiasServiceProvider,
):
    scope = Scope.APP
