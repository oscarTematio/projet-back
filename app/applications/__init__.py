from .resources import application_api
from injector import Module, Key
from .repository import ApplicationRepository
from .resources import ApplicationResource
from .service import ApplicationService


ApplicationApi = Key('ApplicationApi')

class ApplicationModule(Module):
    def configure(self, binder):
        binder.bind(ApplicationResource, to=ApplicationResource)
        binder.bind(ApplicationService, to=ApplicationService)
        binder.bind(ApplicationRepository, to=ApplicationRepository)
        binder.bind(ApplicationApi, to=application_api)

