from injector import Key

from app.applications import ApplicationModule
from app.core.module import CoreModule
from .module import configure
from .db import DatabaseModule, MigrateModule
from .keys import *


all_modules = [configure, CoreModule, DatabaseModule, MigrateModule, ApplicationModule]