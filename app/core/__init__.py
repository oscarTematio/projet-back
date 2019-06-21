from injector import Key

from app.applications import ApplicationModule
from .module import configure
from .db import DatabaseModule, MigrateModule
from .keys import *


all_modules = [configure, DatabaseModule, MigrateModule, ApplicationModule]