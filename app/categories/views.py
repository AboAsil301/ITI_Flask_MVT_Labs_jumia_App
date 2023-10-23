from flask import Flask
from flask import request,render_template,redirect, url_for
from app.models import Categories, db
import os
from werkzeug.utils import secure_filename

# connect blueprint with views
from app.categories import categories_blueprint


UPLOAD_FOLDER = 'static/images/product/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@categories_blueprint.route('hello')
def say_hello():
    return '<h1 style="color:red; text-align:center"> Hello world from Product</h1>'

@categories_blueprint.route('index',endpoint='index', methods=['GET'])
def index():
    categories = Categories.get_all_objects()
    return render_template('products/index.html', categories=categories)


# Function to generate the filename in the format "product-{product_id}.jpg"
def generate_unique_filename(product_id, filename):
    # Extract the file extension from the original filename
    file_extension = os.path.splitext(filename)[1]

    # Combine the product's ID and the desired format
    unique_filename = f"product-{product_id}{file_extension}"
    return unique_filename



## create new object
@categories_blueprint.route('create', methods=['GET', 'POST'], endpoint='create')
def create():
    if request.method == 'POST':
        category = Categories(
            name=request.form['name'],

        )


        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/create.html')



@categories_blueprint.route('/category/<int:id>', endpoint='show')
def category_show(id):
    category = Categories.query.get_or_404(id)
    return render_template('categories/show.html', category=category)


@categories_blueprint.route('edit/<int:id>', endpoint='edit')
def product_edit(id):
    category = Categories.query.get_or_404(id)
    return render_template('categories/edit.html', category=category)


@categories_blueprint.route('edit/<int:id>', methods=['GET', 'POST'], endpoint='update')
def update(id):
    category = Categories.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/edit.html', category=category)


@categories_blueprint.route('delete/<int:id>', endpoint='delete')
def delete(id):
    category = Categories.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.index'))
