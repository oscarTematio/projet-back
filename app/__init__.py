from app.core.module import app as application,Configuration
from app.core import all_modules
from flask_injector import FlaskInjector
from flask_migrate import Migrate
import app.applications.models

flask_injector = FlaskInjector(app=application, modules=all_modules)

# expose migrate to database migration tool
config = flask_injector.injector.get(Configuration)

migrate = flask_injector.injector.get(Migrate)