from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from injector import singleton, Module, provider
from sqlalchemy.exc import DatabaseError
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

def configure(binder):
    binder.bind(Configuration, to=config, scope=singleton)
    binder.bind(App, to=app, scope=singleton)


