from dishka import Provider, Scope, provide_all

from url_alias.application.interactors.url.create import CreateURLInteractor
from url_alias.application.interactors.url.deactivate import DeactivateURLInteractor
from url_alias.application.interactors.url.get_list import GetOwnURLListInteractor
from url_alias.application.interactors.url.redirect import RedirectInteractor
from url_alias.application.interactors.user.login import LoginUserInteractor
from url_alias.application.interactors.user.register import RegisterUserInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(
        RegisterUserInteractor,
        LoginUserInteractor,
        CreateURLInteractor,
        DeactivateURLInteractor,
        GetOwnURLListInteractor,
        RedirectInteractor,
    )
