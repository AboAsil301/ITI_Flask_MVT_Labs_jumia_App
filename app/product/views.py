from flask import Flask
from flask import request,render_template,redirect, url_for
from app.models import Product,Categories, db

import os
from werkzeug.utils import secure_filename

# connect blueprint with views
from app.product import product_blueprint


UPLOAD_FOLDER = 'static/images/product/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@product_blueprint.route('hello')
def say_hello():
    return '<h1 style="color:red; text-align:center"> Hello world from Product</h1>'

@product_blueprint.route('index',endpoint='index', methods=['GET'])
def index():
    products = Product.get_all_objects()
    return render_template('products/index.html', products=products)


# Function to generate the filename in the format "product-{product_id}.jpg"
def generate_unique_filename(product_id, filename):
    # Extract the file extension from the original filename
    file_extension = os.path.splitext(filename)[1]

    # Combine the product's ID and the desired format
    unique_filename = f"product-{product_id}{file_extension}"
    return unique_filename



## create new object
@product_blueprint.route('create', methods=['GET', 'POST'], endpoint='create')
def create():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            instock=request.form.get('instock') == 'on',
            category_id=request.form['category_id'],
        )


        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)

                # Generate a unique filename based on the product ID
                # Assuming you have an ID column as the primary key
                product_id = db.session.query(Product).count() + 1  # Increment product ID
                unique_filename = generate_unique_filename(product_id, filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                file.save(file_path)
                product.image = unique_filename  # Update the product's image in the database

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.index'))

    return render_template('products/create.html', categories=Categories.get_all_objects())



ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@product_blueprint.route('/product/<int:id>', endpoint='show')
def product_show(id):
    product = Product.get_specific_product(id)
    return render_template('products/show.html', product=product)


@product_blueprint.route('edit/<int:id>', endpoint='edit')
def product_edit(id):
    product = Product.get_specific_product(id)
    return render_template('products/edit.html', product=product,categories=Categories.get_all_objects())


@product_blueprint.route('edit/<int:id>', methods=['GET', 'POST'], endpoint='update')
def update(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.instock = request.form.get('instock') == 'on'

        category_id = request.form.get('category_id')
        if category_id is not None:
            # Update the product's category ID
            product.category_id = int(category_id)


        # Check if a new image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])  # Create the directory if it doesn't exist

                if product.image:
                    # Remove the old image if it exists
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Generate a unique filename based on the product ID
                unique_filename = generate_unique_filename(product.id, filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                file.save(file_path)
                product.image = unique_filename  # Update the product's image

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('products.index'))

    return render_template('products/edit.html', product=product)


@product_blueprint.route('delete/<int:id>', endpoint='delete')
def delete(id):
    product = Product.query.get_or_404(id)

    # Remove the product's image file, if it exists
    if product.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.index'))


@product_blueprint.route('contact', methods=['GET'], endpoint='contact')
def contact():
    return render_template('land/contact_us.html')

@product_blueprint.route('abouts', methods=['GET'], endpoint='abouts')
def abouts():
    return render_template('land/about.html')
