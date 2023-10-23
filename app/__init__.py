# import flask
from flask import Flask

# load configuration
from app.config import projectConfig as AppConfig

# get db object
from app.models import  db


def create_app(config_name='dev'):
    app = Flask(__name__)
    # object of config class(DevelopmentConfig or ProductionConfig)from config.py base on config_name
    current_App_Config = AppConfig[config_name]
    # load configuration from current_App_Config object
    app.config.from_object(current_App_Config)
    # initialize db
    db.init_app(app)
    return app
