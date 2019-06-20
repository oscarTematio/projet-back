from unittest import TestCase

from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy

from app import all_modules
from app.core.module import app

from alembic import command, config

import os
import run

ROOT_DIR = os.path.dirname(os.path.abspath(run.__file__))


class AbstractDbTest:

    """
    Abstract class in order to run migrations on an in-memory sqlite db to prepare integration tests
    """
    @classmethod
    def setUpDb(cls):

        # override config to use a mem database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        if not hasattr(cls, 'flask_injector'):
            # initiate injector
            cls.flask_injector = FlaskInjector(app=app, modules=all_modules)

            # retrieve db for populating initial data
            cls.db = cls.flask_injector.injector.get(SQLAlchemy)

            # reconfigure alembic and run the migration with the current connexion (avoiding in-memory db reinit)
            cfg = config.Config(ROOT_DIR+"/migrations/alembic.ini")

            with app.app_context():
                con = cls.db.engine.connect()
                cfg.attributes['connection'] = con
                cfg.set_main_option("script_location", ROOT_DIR+"/migrations")

                command.upgrade(cfg, "head")


        # set app in testing mode
        app.testing = True

        # set app in class for descendant classes
        cls.app = app