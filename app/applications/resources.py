from flask_restplus import Namespace, Resource, fields, reqparse
from .service import ApplicationService
from injector import inject
from flask import request, make_response

application_api = Namespace('applications', description="API managing applications")


application_model_for_list = application_api.model('Application', {
    'name': fields.String,

})

application_model = application_api.model('Application', {
    'app_id': fields.String,
    'name': fields.String,
    'source': fields.String,
    
})


def to_resource_link(res):
    r = ResourceWithLinks(res, application_api)
    r.add_link("self", res.bundle)

    return r


@application_api.route("/")
class ApplicationListResource(Resource):


    """
    Return the list of applications
    """
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

    @inject
    def __init__(self, application_service: ApplicationService, api):
        self.application_service = application_service
        self.api=api

    @application_api.marshal_with(application_model_for_list, envelope="data")
    def get(self):
        apps = self.application_service.get_all()
        return apps

    def post(self):  
        data= ApplicationListResource.parser.parse_args
        app= self.application_service.create_application(data['name'], data['source'])
        try:
            app.application_service.add_to_db(app)
        except:
            return {"failed to add this app "},400

               

        

@application_api.route("/<string:bundle>")
class ApplicationResource(Resource):
    """
    Returns the representation of a specific application
    """
    @inject
    def __init__(self, application_service: ApplicationService, api):
        self.application_service = application_service
        self.api=api

    @application_api.marshal_with(application_model)
    def get(self, bundle):
        app = self.application_service.get_by_bundle(bundle)

        res=ResourceWithLinks(app, application_api)
        res.add_link("self", bundle)
        res.add_link("picture", bundle+"/picture")
        res.add_link("list")
        return res


@application_api.route("/<string:bundle>/picture")
class ApplicationPictureResource(Resource):

    """
    Returns the picture of an application
    """
    @inject
    def __init__(self, application_service: ApplicationService, api):
        self.application_service = application_service
        self.api = api

    def get(self, bundle):

        bytes = self.application_service.get_application_image(bundle)

        r = make_response(bytes)

        r.mimetype = "image/png"

        return r





