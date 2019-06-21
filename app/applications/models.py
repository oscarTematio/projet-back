from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, UniqueConstraint
from app.core.db import metadata
from sqlalchemy.orm import mapper 


application = Table('application', metadata,
                    Column('app_id', Integer, primary_key=True, autoincrement=True),
                    Column('name',String(80), nullable=False),
                    Column('source',String(80), nullable=False),
                    Column('version',String(10))                   
)

class ApplicationModel(object):

    #initialize the table 
    def __init__(self, name,source,version):
        self.app_id = None
        self.name = name
        self.source = source
        self.version=version




mapper(ApplicationModel, application)



