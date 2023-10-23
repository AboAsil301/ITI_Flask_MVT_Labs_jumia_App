from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# here where I will create the models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer ,default=100)
    instock = db.Column(db.Boolean)
    # created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    #another way to create column
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now(), server_default=db.func.now())
