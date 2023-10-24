# create new blueprint
from flask import  Blueprint
categories_blueprint= Blueprint('categories', __name__, url_prefix='/categories/')
from app.categories import views
