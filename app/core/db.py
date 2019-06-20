from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from injector import Module, provider, singleton
from sqlalchemy.exc import DatabaseError

from .keys import *

# Declare the global metadata for SQLAlchemy models
metadata = MetaData()


class DatabaseModule(Module):
    @provider
    @singleton
    def provide_db(self, app: App) -> SQLAlchemy:
        # Bootstrap SQL alchemy
        db =  SQLAlchemy(app)

        return db


class MigrateModule(Module):

    @provider
    @singleton
    def provide_migrate(self, app:App, db: SQLAlchemy) -> Migrate:
        # migrate the db
        return Migrate(app, db)

