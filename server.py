from flask import Flask
from flask_app import app       #Importing app variable from __init__.py

#Import all controllers in controllers folder
from flask_app.controllers import user_controller
from flask_app.controllers import recipe_controller


if __name__ == "__main__":
    app.run(debug = True)
# This code is needed to run your environment and be in an active state when you run this file.