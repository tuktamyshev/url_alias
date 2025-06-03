from dishka import Provider, Scope, provide

from url_alias.domain.services.access import AccessService


class DomainServicesProvider(Provider):
    scope = Scope.APP

    access_service = provide(AccessService)
