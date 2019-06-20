from flask_testing import TestCase

from app.applications.models import Application
from test.abstract_db_test import AbstractDbTest

class AbstractFunctionalTest(AbstractDbTest,TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractDbTest.setUpDb()

    def create_app(self):
        return AbstractDbTest.app

    def tearDown(self):
        AbstractDbTest.db.session.rollback()
        AbstractDbTest.db.session.query(Application).delete()
        AbstractDbTest.db.session.commit()


