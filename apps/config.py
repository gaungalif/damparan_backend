from multiprocessing.util import abstract_sockets_supported
import os
from sqlite3 import SQLITE_ALTER_TABLE

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    

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
    