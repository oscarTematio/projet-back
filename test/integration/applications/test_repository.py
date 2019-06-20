from test.integration.abstract_integration_test import AbstractIntegrationTest

from app.applications.repository import ApplicationRepository
from app.applications.models import Application

class ApplicationRepositoryTestCase(AbstractIntegrationTest):
    """
    Test for the applicaton repository
    """

    def setUp(self):
        self.application_repository = ApplicationRepositoryTestCase.flask_injector.injector.get(ApplicationRepository)

    def test_get_all(self):
        # given
        application = Application(name="Test", bundle="test.app", version="1.0.0", description="1.0.0", picture="==picture==")
        ApplicationRepositoryTestCase.db.session.add(application)

        # when
        results = self.application_repository.get_all()

        # then
        expected = Application(name="Test", bundle="test.app", version="1.0.0", description="1.0.0", picture="==picture==")
        expected.id = 1
        self.assertListEqual([expected], results)

    def test_save(self):
        application = Application(name="Test", bundle="test.app", version="1.0.0", description="1.0.0", picture="==picture==")

        self.application_repository.save(application)

        all_apps = ApplicationRepositoryTestCase.db.session.query(Application).all()

        self.assertEqual(1, len(all_apps))

    def test_delete(self):
        # given
        application = Application(name="Test", bundle="test.app", version="1.0.0", description="1.0.0",
                                  picture="==picture==")
        ApplicationRepositoryTestCase.db.session.add(application)
        ApplicationRepositoryTestCase.db.session.flush()

        # when
        results = self.application_repository.delete(application)

        # then
        all_apps = ApplicationRepositoryTestCase.db.session.query(Application).all()
        self.assertEqual(0,len(all_apps))

    def test_find_application_by_bundle(self):
        # given
        session = ApplicationRepositoryTestCase.db.session
        session.add(Application(name="Test", bundle="test.app", version="1.0.0"))
        app2 = Application(name="Test 2", bundle="test.app.2", version="2.0.0")
        session.add(app2)
        ApplicationRepositoryTestCase.db.session.flush()

        # when
        queried_app = self.application_repository.find_application_by_bundle("test.app.2")

        # then
        self.assertEqual(app2, queried_app)