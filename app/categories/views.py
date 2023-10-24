from flask import Flask
from flask import request,render_template,redirect, url_for
from app.models import Categories, db

# connect blueprint with views
from app.categories import categories_blueprint


@categories_blueprint.route('hello')
def say_hello():
    return '<h1 style="color:red; text-align:center"> Hello world from Categories</h1>'

@categories_blueprint.route('index',endpoint='index', methods=['GET'])
def index():
    categories = Categories.get_all_objects()
    return render_template('categories/index.html', categories=categories)


## create new object
@categories_blueprint.route('create', methods=['GET', 'POST'], endpoint='create')
def create():
    if request.method == 'POST':
        Categories.save_category(request.form)
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
