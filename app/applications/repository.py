from .models import ApplicationModel
from flask_sqlalchemy import SQLAlchemy
from injector import inject

class ApplicationRepository:
    """Persistence of applications"""

    @inject
    def __init__(self, db: SQLAlchemy):
        self._db = db
        
        

    def get_all(self):
        return self._db.session.query(ApplicationModel).all()

    def json(self):
        return {'name': self.name, 'source': self.source}

    def find_application_by_id(self, _id):
        return self._db.session.query(ApplicationModel).filter(ApplicationModel.app_id == _id).first()

    def find_application_by_name(self, name):
        return self._db.session.query(ApplicationModel).filter(ApplicationModel.name == name).first()
    
    def create_app(self,name,source):
        return ApplicationModel(name,source)
        
    def _update_application(self,_id,object):
        return self._db.session.query(ApplicationModel).filter(ApplicationModel.app_id ==_id).update(object)

    def save_to_db(self, object):
        self._db.session.add(object)
        self._db.session.commit()

    def delete(self, object):
        self._db.session.delete(object)
        self._db.session.commit()
  

    def flush(self):
        self._db.session.flush()