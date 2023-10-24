from flask_sqlalchemy import SQLAlchemy
from flask import  url_for

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

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Categories', backref='products_list')
    def __str__(self):
        return f"{self.name}"

    # def get_image_url(self):
    #     return  f'images/product/{self.image}'

    @property
    def get_image_url(self):
        return url_for('static', filename=f'images/product/{self.image}') if self.image else url_for('static',
                                                                                                     filename='images/product/placeholder.png')

    @classmethod
    def get_all_objects(cls):
        return cls.query.all()

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_product(cls, request_form):
        product = cls(**request_form)
        db.session.add(product)
        db.session.commit()
        return product

    @classmethod
    def get_specific_product(cls, id):
        return  cls.query.get_or_404(id)


    @property
    def get_show_url(self):
        return  url_for('products.show', id=self.id)

    @property
    def get_delete_url(self):
        return  url_for('products.delete', id= self.id)

    @property
    def get_edit_url(self):
        return  url_for('products.edit', id= self.id)



class Categories(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_onupdate=db.func.now(), server_default=db.func.now())
    products = db.relationship('Product', backref='product_name', lazy=True)


    def __str__(self):
        return f"{self.name}"
    @classmethod
    def get_all_objects(cls):
        return  cls.query.all()

    @classmethod
    def save_category(cls, request_data):
        category  =cls(**request_data)
        db.session.add(category)
        db.session.commit()
        return category
