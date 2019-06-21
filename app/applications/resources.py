from flask_restplus import Namespace, Resource, fields, reqparse, abort
from .service import ApplicationService
from injector import inject
from flask import request, make_response


application_api = Namespace('applications', description="API managing applications")


application_model_for_list = application_api.model('Application', {
    'name': fields.String,

})

application_model = application_api.model('Application', {
    'name': fields.String,
    'source': fields.String,
    
})

class Parse:
    parser = reqparse.RequestParser()
    parser.add_argument('source',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

@application_api.route("/")
class ApplicationListResource(Resource):
    """
    Return the list of applications
    """
    @inject
    def __init__(self, application_service: ApplicationService, api):
        self.application_service = application_service
        self.api=api


    @application_api.marshal_with(application_model_for_list, envelope="Applicaitons")
    def get(self):
        apps = self.application_service.get_all()
        return apps


    @application_api.marshal_with(application_model, envelope="Application")
    def post(self):  
        data= Parse.parser.parse_args()
        application = self.application_service.create_application(data['name'], data['source'])
        self.application_service.add_to_db(application)
        return application, 201
               

        

@application_api.route("/<int:_id>")
class ApplicationResource(Resource):
    """
    Returns the representation of a specific application
    """

    @inject
    def __init__(self, application_service: ApplicationService, api):
        self.application_service = application_service
        self.api=api

    @application_api.marshal_with(application_model)
    def get(self, _id):
        app = self.application_service.get_by_id(_id)
        return app

    
    @application_api.marshal_with(application_model)
    def put(self, _id):
        data =Parse.parser.parse_args()
        self.application_service.update_application(_id, data)
        return data

    def delete(self,_id):
        app= self.application_service.delete_application(_id)
        return app
        




    





