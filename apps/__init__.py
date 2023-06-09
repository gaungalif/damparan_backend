from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from importlib import import_module
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
# login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    # login_manager.init_app(app)
    
def register_blueprints(app):
    for module_name in ('pesantren', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
        
def configure_database(app):
    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        
def create_app(config_filename):
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_object(config_filename)
    
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    
    return app