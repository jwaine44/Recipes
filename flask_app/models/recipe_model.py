from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
from flask import flash, session
from flask_app.models import user_model

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30_minutes = data['under_30_minutes']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # self.users = []
#        ADD ABOVE TO TEMPLATE Above is needed for a many to many relationship, need to have a list in case we want to show which burgers are related to the topping; refer to get_topping_with_burgers below



    # CREATE
    # Creating a new row of information in the table
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes(name, description, under_30_minutes, instructions, created_at, user_id) VALUES(%(name)s, %(description)s, %(under_30_minutes)s, %(instructions)s, %(created_at)s, %(user_id)s);"
        return connectToMySQL(database).query_db(query, data)



#     RETRIEVE
#     Retrieving all information from a table
    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL(database).query_db(query)

        list_recipes = []

        if len(results) > 0:
            for recipe in results:
                list_recipes.append(cls(recipe))
        return list_recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        single_result = connectToMySQL(database).query_db(query, data)

        if len(single_result) > 0:
            return cls(single_result[0])
        else:
            return None

#     Another use of RETRIEVE, this time with two tables together
#     LEFT JOIN joining the ninjas table to the dojo table; this was done for the dropdown in Dojos and Ninjas
#     @classmethod
#     def display_dojo(cls, data):
#         query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
#         single_result = connectToMySQL(database).query_db(query, data)

#         ninjas = []

#         for ninja in single_result:
#             ninjas.append(Ninja(ninja))

#         return ninjas

#    Another use of RETRIEVE, this one time with a many to many relationship
#    LEFT JOIN joining three tables together by the new table that's created by the many to many relationship; here the new table is add_ons
#    Retrieves the specific topping along with all the burgers associated with it
    @classmethod
    def get_recipes_with_users(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN recipes_users ON recipes_users.recipe_id = recipes.id LEFT JOIN users ON recipes_users.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(database).query_db(query, data)
        # results will be a list of recipe objects with the user attached to each row. 
        recipe = cls(results[0])
        for row_from_db in results:
            # Now we parse the user data to make instances of users and add them into our list.
            user_data = {
                "id": row_from_db["users.id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            }
            recipe.users.append(user_model.User(user_data))
        return recipe



#     UPDATE
#     Updating a row of information in the table; match all the relevant rows in the table to the rows in the query below
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_minutes = %(under_30_minutes)s, instructions = %(instructions)s, created_at = %(created_at)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(database).query_db(query, data)



    # DELETE
    # Deleting a row from the table
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(database).query_db(query, data)

    @staticmethod
    def validate_create_recipe(data):
        isValid = True
        if data['name'] == "":
            flash("You must provide a recipe name.", "error_recipe_name")
            isValid = False
        if len(data['name']) < 3:
            flash("You must provide a recipe name with more than 3 characters.", "error_recipe_name")
            isValid = False
        if data['description'] == "":
            flash("You must provide a recipe description.", "error_recipe_description")
            isValid = False
        if len(data['description']) < 3:
            flash("You must provide a recipe description with more than 3 characters.", "error_recipe_description")
            isValid = False
        if data['instructions'] == "":
            flash("You must provide recipe instructions.", "error_recipe_instructions")
            isValid = False
        if len(data['instructions']) < 3:
            flash("You must provide a recipe description that's at least 3 characters long.", "error_recipe_instructions")
            isValid = False
        if data['created_at'] == "":
            flash("You must provide a date you made this recipe.", "error_recipe_created_at")
        return isValid

    @staticmethod
    def validate_edit_recipe(data):
        isValid = True
        if data['name'] == "":
            flash("You must provide a recipe name.", "error_recipe_name")
            isValid = False
        if len(data['name']) < 3:
            flash("You must provide a recipe name with more than 3 characters.", "error_recipe_name")
            isValid = False
        if data['description'] == "":
            flash("You must provide a recipe description.", "error_recipe_description")
            isValid = False
        if len(data['description']) < 3:
            flash("You must provide a recipe description with more than 3 characters.", "error_recipe_description")
            isValid = False
        if data['instructions'] == "":
            flash("You must provide recipe instructions.", "error_recipe_instructions")
            isValid = False
        if len(data['instructions']) < 3:
            flash("You must provide a recipe description that's at least 3 characters long.", "error_recipe_instructions")
            isValid = False
        if data['created_at'] == None:
            flash("You must provide a date you made this recipe.", "error_recipe_date_made")
        return isValid