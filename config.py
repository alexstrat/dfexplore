# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data/app.db')
DATABASE_CONNECT_OPTIONS = {}
DEBUG = True

DATA_DIR = os.path.join(BASE_DIR, 'data')
