from flask import session, render_template, request, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def display_login():
    if User.validate_session():
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def user_login():
    if User.validate_login(request.form) == False:
        return redirect('/')
    else:
        result = User.get_one_user(request.form)

        if result == None:
            flash("Wrong credentials", "error_login")
            return redirect('/')
        else:
            if not bcrypt.check_password_hash(result.password, request.form['password']):
                flash("Wrong credentials", "error_login")
                return redirect('/')
            else:
                session['first_name'] = result.first_name
                session['last_name'] = result.last_name
                session['email'] = result.email
                session['user_id'] = result.id
                return redirect('/dashboard')

@app.route('/register/user', methods=['POST'])
def register():
    if User.validate_registration(request.form) == False:
        return redirect('/dashboard')
    else:
        if User.get_one_user({"email": request.form['email']}) == None:
            data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            }
            user_id = User.create_user(data)
            session['first_name']: request.form['first_name']
            session['last_name']: request.form['last_name']
            session['email']: request.form['email']
            session['id']: user_id
            return redirect('/dashboard')
        else:
            flash("This email is already in use. Please type a different one.", "error_register_email")
            return redirect('/')

@app.route('/logout')
def user_logout():
    session.clear()
    return redirect('/')