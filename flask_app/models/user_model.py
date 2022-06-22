from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
import re
from flask import flash, session
from flask_app.models import recipe_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(database).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def create_user(cls, data):
        query = "INSERT into users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes_users ON recipes_users.user_id = users.id LEFT JOIN recipes ON recipes_users.recipe_id = recipes.id WHERE users.id = %(id)s;"
        results = connectToMySQL(database).query_db(query, data)
        # results will be a list of recipe objects with the user attached to each row. 
        if len(results) > 0:
            current_user = cls(results[0])
            list_recipes = []
            for row_from_db in results:
            # Now we parse the user data to make instances of users and add them into our list.
                recipe_data = {
                    "id": row_from_db["recipes.id"],
                    "name": row_from_db["name"],
                    "description": row_from_db["description"],
                    "under_30_minutes": row_from_db["under_30_minutes"],
                    "instructions": row_from_db["instructions"],
                    "date_made": row_from_db["date_made"],
                    "created_at": row_from_db["recipes.created_at"],
                    "updated_at": row_from_db["recipes.updated_at"]
                }
            recipe = recipe_model.Recipe(recipe_data)
            list_recipes.append(recipe)
            current_user = list_recipes
            return current_user
        return None

    @staticmethod
    def validate_registration(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide a first name.", "error_register_first_name")
            isValid = False
        if len(data['first_name']) < 2:
            flash("You must provide a first name with more than 2 characters.", "error_register_first_name")
            isValid = False
        if data['last_name'] == "":
            flash("You must provide a last name.", "error_register_last_name")
            isValid = False
        if len(data['last_name']) < 2:
            flash("You must provide a first name with more than 2 characters.", "error_register_last_name")
            isValid = False
        if data['email'] == "":
            flash("You must provide an email.", "error_register_email")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_register_email")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_register_password")
            isValid = False
        if len(data['password']) < 8:
            flash("You must provide a password that's at least 8 characters long.", "error_register_password")
            isValid = False
        if data['password_confirmation'] != data['password']:
            flash("Your password confirmation doesn't match.", "error_register_password_confirmation")
            isValid = False
        return isValid

    @staticmethod
    def validate_login(data):
        isValid = True
        if data['email'] == "":
            flash("Please provide your email.", "error_email_login")
            isValid = False
        if data['password'] == "":
            flash("Please provide your password.", "error_password_login")
            isValid = False
        return isValid

    @staticmethod
    def validate_session():
        if "user_id" not in session:
            return False
        else:
            return True
    
    @staticmethod
    def validate_user(user):
        isValid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            isValid = False
        return isValid