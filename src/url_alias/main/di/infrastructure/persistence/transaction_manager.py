from dishka import Provider, Scope, provide

from url_alias.application.interfaces.transaction_manager import TransactionManager
from url_alias.infrastructure.persistence.adapters.transaction_manager import SqlAlchemyTransactionManager


class SQLAlchemyTransactionManagerProvider(Provider):
    transaction_manager = provide(SqlAlchemyTransactionManager, provides=TransactionManager, scope=Scope.REQUEST)
