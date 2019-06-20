from app.applications.models import Application
from test.functional.abstract_functional_test import AbstractFunctionalTest
from app.core.module import app

class ApplicationApiTest(AbstractFunctionalTest):


    def test_get_all_applications(self):
        existing_app = Application(name="testapp2", bundle="test.app.2", version="1.0.0")
        ApplicationApiTest.db.session.add(existing_app)
        ApplicationApiTest.db.session.flush()
        response = self.client.get('/applications/?repository_update=true')

        json = response.json
        data = json['data']

        self.assertIsNotNone(data)
        self.assertEqual(2, len(data))
        self.assertEqual('testapp', data[0]['name'])
        self.assertEqual('testapp2', data[1]['name'])
        self.assertEqual('test.app.2', data[1]['bundle'])

    def test_get_application(self):
        existing_app = Application(name="testapp2", bundle="test.app.2", version="1.0.0")
        ApplicationApiTest.db.session.add(existing_app)
        ApplicationApiTest.db.session.flush()

        response = self.client.get('/applications/test.app.2')

        json = response.json

        self.assertEqual('test.app.2', json['bundle'])

    def test_get_application_picture(self):
        existing_app = Application(name="testapp2", bundle="test.app.2", version="1.0.0", picture="AQID")
        ApplicationApiTest.db.session.add(existing_app)
        ApplicationApiTest.db.session.flush()

        response = self.client.get('/applications/test.app.2/picture')

        data = response.data

        self.assertEqual(bytearray([0x01,0x02,0x03]), data)

