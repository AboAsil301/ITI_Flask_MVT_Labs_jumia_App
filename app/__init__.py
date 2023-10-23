# import flask
from flask import Flask

# load configuration
from app.config import projectConfig as AppConfig

# get db object
from app.models import  db

# get views
# from app.product.views import say_hello

# get blueprint
from app.product import product_blueprint

#import templates render
from flask import render_template

def create_app(config_name='dev'):
    app = Flask(__name__)
    # object of config class(DevelopmentConfig or ProductionConfig)from config.py base on config_name
    current_App_Config = AppConfig[config_name]
    # load configuration from current_App_Config object
    app.config.from_object(current_App_Config)
    # initialize db
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html')

    # initialize routes
    # app.add_url_rule('/hello', view_func=say_hello)
    ## register blueprint in the application
    app.register_blueprint(product_blueprint)
    return app
