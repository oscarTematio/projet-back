from unittest import TestCase
from unittest.mock import Mock

from flask import Flask
from flask_injector import FlaskInjector

from injector import Module, provider, singleton

from app import all_modules, Configuration
from app.applications import ApplicationService, ApplicationApi, ApplicationModule
from app.applications.models import Application
from app.applications import application_api as application_api
from flask_restplus import Api

import config


def configure_config(binder):
    binder.bind(Configuration, to=config, scope=singleton)


class ServiceMockModule(Module):
    def __init__(self, mock):
        self.mock = mock

    @provider
    @singleton
    def provide_mock(self) -> ApplicationService:
        return self.mock


class ApplicationResourceTestCase(TestCase):

    def setUp(self):
        app = Flask(__name__, instance_relative_config=True)
        # Load the config file
        app.config.from_object(config)

        # Initiate the Flask API
        api = Api(
            title='Box API',
            version='1.0',
            description='Box API',
            # All API metadatas
        )

        # Load application namespace
        api.add_namespace(application_api, path="/applications")

        # Bootstrap app
        api.init_app(app)

        self.service_mock=Mock(spec=ApplicationService)
        modules = [configure_config, ApplicationModule, ServiceMockModule(self.service_mock)]
        self.injector = FlaskInjector(app=app, modules=modules)

        self.client = app.test_client()

    def test_get_application_list(self):
        app = Application(name="Test", bundle="test.app", version="1.0.0", description="desc", picture="==picture==")
        app.id = 1
        self.service_mock.get_all.return_value = [app]

        response = self.client.get("/applications/")

        self.service_mock.get_all.assert_called_once_with()

        self.assertEqual({ 'data': [{'bundle': 'test.app',
                               'name': 'Test',
                               'links': [
                                   {
                                       'rel': 'self',
                                        'href': 'http://localhost/applications/test.app'
                                   }
                               ]}]
                           },
                         response.json)

    def test_get_application_list_with_repo_update(self):
        self.service_mock.get_all.return_value = [
            Application(name="Test", bundle="test.app", version="1.0.0", description="1.0.0", picture="==picture==")]

        self.client.get("/applications/?repository_update=true")

        self.service_mock.get_all.assert_called_once_with(repository_update=True)


    def test_get_application(self):
        self.service_mock.get_by_bundle.return_value = \
            Application(id=1, name="Test", bundle="test.app", version="1.0.0", description="desc", picture="==picture==")

        response = self.client.get("/applications/test.app")

        self.service_mock.get_by_bundle.assert_called_once_with("test.app")
        self.assertEqual({'version': '1.0.0',
                          'bundle': 'test.app',
                          'description': 'desc',
                          'name': 'Test',
                          'links': [
                              {'rel': 'self', 'href': 'http://localhost/applications/test.app'},
                              {'rel': 'picture', 'href': 'http://localhost/applications/test.app/picture'},
                              {'rel': 'list', 'href': 'http://localhost/applications/'}
                          ]},
                         response.json)

    def test_get_application_picture(self):
        self.service_mock.get_application_image.return_value = bytearray([0x01, 0x02, 0x03])

        response = self.client.get("/applications/test.app/picture")

        self.assertEqual('image/png', response.headers['content-type'])
        self.assertEqual(bytearray([0x01, 0x02, 0x03]), response.data)

        self.service_mock.get_application_image.assert_called_once_with("test.app")