from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from injector import singleton, Module, provider
from sqlalchemy.exc import DatabaseError

from app.core.ipfs_client import IpfsClient
from .keys import Configuration, App

from app.applications import application_api as application_api

import config


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


@app.after_request
def session_commit(response, db: SQLAlchemy):
    if response.status_code >= 400:
        return response
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise

    return response



def configure(binder):
    binder.bind(Configuration, to=config, scope=singleton)
    binder.bind(App, to=app, scope=singleton)

class CoreModule(Module):

    @provider
    @singleton
    def provide_ipfs_client(self, config: Configuration) -> IpfsClient:
        return IpfsClient(config)



