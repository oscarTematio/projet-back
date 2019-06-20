from unittest.mock import Mock, call

from app.applications.models import Application, Container
from app.applications.service import ApplicationService
from app.applications.repository import ApplicationRepository
from app.core.ipfs_client import IpfsClient
from test.unit.abstract_unit_test import AbstractUnitTest
import json
import config


class ApplicationServiceTest(AbstractUnitTest):
    """ Test of the application service"""

    def setUp(self):
        self.ipfs_client_mock = Mock(spec=IpfsClient)

        self.application_repository_mock = Mock(spec=ApplicationRepository)

        self.application_service = ApplicationService(self.application_repository_mock, self.ipfs_client_mock, config)

    def test_get_all(self):
        self.application_repository_mock.get_all.return_value = [ {"name": "test"} ]

        apps = self.application_service.get_all()

        self.assertEqual([ {"name": "test"} ], apps)
        self.application_repository_mock.get_all.assert_called_once_with()


    def test_get_all_with_repository_update(self):

        #given
        config.BOX_REPOSITORY_IPN="/ipns/ANIPNPOINTER"
        descriptor = self.load_json_resource("sample_descriptor.json")
        self.ipfs_client_mock.get_json_content.return_value=descriptor

        # when
        self.application_service.get_all(repository_update=True)

        # then
        self.ipfs_client_mock.get_json_content.assert_called_once_with("/ipns/ANIPNPOINTER")
        app1 = Application(name="Test App", bundle="test.app", description="Lorem ipsum", version="1.0.0", picture="==BASE64ENCODEDIMAGE==")
        app2 = Application(name="Test App 2", bundle="test.app.2", description="Lorem ipsum 2", version="2.0.0", picture="==BASE64ENCODEDIMAGE2==")
        containers1 = [Container(image="anipfshash/busybox:latest", application=app1),
                       Container(image="asecondipfshash/busybox:latest", application=app1)]
        containers2 = [Container(image="athirdipfshash/busybox:latest", application=app2)]
        app1.containers = containers1
        app2.containers = containers2

        self.application_repository_mock.save.assert_has_calls([
            call(Container(image="anipfshash/busybox:latest", application=app1)),
            call(Container(image="asecondipfshash/busybox:latest", application=app1)),
            call(app1),
            call(Container(image="athirdipfshash/busybox:latest", application=app2)),
            call(app2)
        ])

    def test_repository_update_with_existing_app(self):
        #given
        app = Application(name="Test", bundle="test.app", version="1.0.0")
        self.application_repository_mock.find_application_by_bundle.return_value=app
        self.ipfs_client_mock.get_json_content.return_value = { 'applications': [ { 'name': 'Test', 'version': '2.0.0', 'bundle': "test.app", 'containers':[]} ]}

        # when
        self.application_service.get_all(repository_update=True)

        # then
        self.application_repository_mock.find_application_by_bundle.assert_called_once_with('test.app')
        self.application_repository_mock.delete.assert_called_once_with(app)
        self.application_repository_mock.flush.assert_called_once_with()
        self.application_repository_mock.save.assert_called_once_with(Application(name="Test", version="2.0.0", bundle="test.app"))

    def test_get_by_bundle(self):
        # given
        app = Application(name="Test", bundle="test.app", version="1.0.0")
        self.application_repository_mock.find_application_by_bundle.return_value = app

        # when
        result = self.application_service.get_by_bundle("bundle.id")

        # then
        self.assertEqual(app, result)
        self.application_repository_mock.find_application_by_bundle.assert_called_once_with("bundle.id")

    def test_get_application_image(self):
        # given
        self.application_repository_mock.find_application_by_bundle.return_value = \
            Application(name="description", bundle="test.app", version="1.0.0", picture="AQID")

        # when
        image = self.application_service.get_application_image("test.app")

        # then
        self.assertEqual( bytearray([0x01,0x02,0x03]), image)

