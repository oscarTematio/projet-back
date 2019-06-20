from app.applications.models import ApplicationModel
from flask_restplus import reqparse
from app.core.keys import Configuration
from app.core.ipfs_client import IpfsClient
from .repository import ApplicationRepository
from injector import inject


class ApplicationService:
    """ Service layer for applications"""

    @inject
    def __init__(self, application_repository: ApplicationRepository, configuration: Configuration):
        self.application_repository = application_repository
        self.configuration = configuration

    def get_all(self):
        return self.application_repository.get_all()


    def get_by_id(self, _id):
        return self.application_repository.find_application_by_id(_id)
    
    def get_by_name(self, name):
        return self.application_repository.find_application_by_name(name)

    def create_application(self,name, source):

        app = self.application_repository.find_application_by_name(name)
        if app is None:
            self.application_repository.create_app(name, source) 
        else:                                                                   
            return {"An aplication with this name already exists"},400
        
        return {"application created"},201

    def add_to_db(self,object):
        return self.application_repository.save_to_db(object)   
        
        
        