from dishka import Provider, Scope, provide

from url_alias.infrastructure.persistence.db_provider import get_engine, get_session, get_sessionmaker


class SQLAlchemyDatabaseProvider(Provider):
    db_engine = provide(staticmethod(get_engine))
    db_sessionmaker = provide(staticmethod(get_sessionmaker))
    db_session = provide(staticmethod(get_session), scope=Scope.REQUEST)
