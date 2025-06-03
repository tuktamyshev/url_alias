from dishka import Provider, Scope, provide

from url_alias.application.interfaces.alias_service import AliasServiceInterface
from url_alias.infrastructure.alias_service import AliasService


class ALiasServiceProvider(Provider):
    alias_service = provide(AliasService, provides=AliasServiceInterface, scope=Scope.REQUEST)
