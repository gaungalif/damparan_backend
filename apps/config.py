from multiprocessing.util import abstract_sockets_supported
import os
from sqlite3 import SQLITE_ALTER_TABLE

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://damparan:damparan@/damparan?unix_socket=/cloudsql/damparan-app2:us-central1:damparan' 
    CORS_HEADERS = 'Content-Type'
    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    

    
    # HOST = str(os.environ.get("DB_HOST"))
    # DATABASE = str(os.environ.get("DB_DATABASE"))
    # USERNAME = str(os.environ.get("DB_USERNAME"))
    # PASSWORD = str(os.environ.get("DB_PASSWORD"))
    # SECRET_KEY  = str(os.environ.get("SECRET_KEY"))
    CORS_HEADERS = 'Content-Type'
    # JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'upload')
    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    
    # MySQL database    
    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo' 

class DebugConfig(Config):
    DEBUG = True
    TESTING = True
    
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_DURATION = 3600
    
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
}
    