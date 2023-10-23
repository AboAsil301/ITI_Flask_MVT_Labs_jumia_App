# connect blueprint with views
from app.product import product_blueprint

@product_blueprint.route('hello')
def say_hello():
    return '<h1 style="color:red; text-align:center"> Hello world from Product</h1>'
