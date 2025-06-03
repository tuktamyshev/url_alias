from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from url_alias.application.interfaces.repositories.url import URLRepository
from url_alias.application.interfaces.repositories.user import UserRepository
from url_alias.infrastructure.config.asgi import ASGIConfig
from url_alias.infrastructure.persistence.adapters.url import SQLAlchemyURLRepository
from url_alias.infrastructure.persistence.adapters.user import SQLAlchemyUserRepository


class SQLAlchemyRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return SQLAlchemyUserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def url_repository(self, session: AsyncSession, asgi_config: ASGIConfig) -> URLRepository:
        return SQLAlchemyURLRepository(session=session, asgi_config=asgi_config)
