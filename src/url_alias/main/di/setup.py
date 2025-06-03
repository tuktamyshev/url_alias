from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from url_alias.infrastructure.config.main_config import Config
from url_alias.main.di.domain_services import DomainServicesProvider
from url_alias.main.di.infrastructure.provider import InfrastructureProvider
from url_alias.main.di.interactors import InteractorsProvider


def setup_web_di(app: FastAPI) -> None:
    config = app.state.config

    container = web_container_factory(config=config)

    setup_dishka(container, app)


def web_container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        InfrastructureProvider(),
        InteractorsProvider(),
        DomainServicesProvider(),
        FastapiProvider(),
        context={Config: config},
    )
