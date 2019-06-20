from app.applications.models import Application
from test.abstract_db_test import AbstractDbTest

from unittest import TestCase

class AbstractIntegrationTest(TestCase, AbstractDbTest):

    @classmethod
    def setUpClass(cls):
        AbstractDbTest.setUpDb()

    def tearDown(self):
        AbstractDbTest.db.session.rollback()
        AbstractDbTest.db.session.query(Application).delete()
        AbstractDbTest.db.session.commit()


