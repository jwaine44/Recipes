from flask import session, render_template, request, redirect
from flask_app import app

# Import model
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User

# CREATE
@app.route('/recipes/new')
def display_create_recipe():
    if User.validate_session() == False:
        return redirect('/')
    else:
        return render_template('add_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create():
    if Recipe.validate_create_recipe(request.form) == False:
        return redirect('/recipes/new')
    else:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'under_30_minutes': request.form['under_30_minutes'],
            'instructions': request.form['instructions'],
            'created_at': request.form['created_at'],
            'user_id': session['user_id']
        }
        Recipe.create_recipe(data)
        return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def display_one_recipe(id):
    if User.validate_session() == False:
        return redirect('/')
    else:
        data = {
            'id': id
        }
        recipe = Recipe.get_one_recipe(data)
        return render_template("instructions.html", recipe = recipe)

@app.route('/dashboard')
def display_dashboard():
    if User.validate_session():
        recipes = Recipe.get_all_recipes()
        return render_template('dashboard.html', recipes = recipes)
    else:
        return redirect('/')

@app.route('/recipes/edit/<int:id>')
def display_edit_recipe(id):
    if User.validate_session() == False:
        return redirect('/')
    else:
        data = {
            'id': id
        }
        recipe = Recipe.get_one_recipe(data)
        return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if Recipe.validate_edit_recipe(request.form) == False:
        return redirect(request.referrer)
    else:
        data = {
            'id': id,
            'name': request.form['name'],
            'description': request.form['description'],
            'under_30_minutes': request.form['under_30_minutes'],
            'instructions': request.form['instructions'],
            'created_at': request.form['created_at'],
            'user_id': session['user_id']
        }
        Recipe.update_recipe(data)
        return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')