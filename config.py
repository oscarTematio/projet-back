import os

# Enable Flask's debugging features. Should be False in production
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/bsf_test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS=True
DATABASE_CONNECT_OPTIONS = {}


THREADS_PER_PAGE = 2




