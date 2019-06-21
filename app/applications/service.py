from app.applications.models import ApplicationModel 
from flask_restplus import reqparse
from app.core.keys import Configuration
from .repository import ApplicationRepository 
from injector import inject
from flask_restplus import abort


class ApplicationService(object):
    """ Service layer for applications"""

    @inject
    def __init__(self, application_repository: ApplicationRepository, configuration: Configuration):
        
        self.application_repository = application_repository
        self.configuration = configuration

    def get_all(self):
        return self.application_repository.get_all()

    def get_by_id(self, _id):
        app = self.application_repository.find_application_by_id(_id)
        if app is None: 
            return abort(409,"Application Not found")
        
        return self.application_repository.find_application_by_id(_id)
    def get_by_name(self, name):
        return self.application_repository.find_application_by_name(name)

    def create_application(self,name, source):
        app = self.application_repository.find_application_by_name(name)
        print (app)
        if  app:
            return abort(409,"An Application with the name {} Already exits ".format(name))
        else:                                                                   
            application = self.application_repository.create_app(name, source)

        return application


    def update_application(self,_id, data):
        app = self.application_repository.find_application_by_id(_id)
        if app:
            try: 
                self.application_repository._update_application(_id, data)
                return self.create_application(data.name, data.source)
            except Exception as Error:
                return Error 
        else:
            return abort(409,"Application Not found")
          
    
    def delete_application(self, _id):
        application = self.application_repository.find_application_by_id(_id)
        if application:
            self.application_repository.delete(application)
            return {"message":"Application deleted Succesfuly"},200
        else:
            return abort(409,"Application Not found")

    def add_to_db(self,object):
        try: 
            return self.application_repository.save_to_db(object)
        except Exception as Error:
            return Error
               
        
        
        