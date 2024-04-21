#__init__.py lets Python know that all files in same directory can be accessed in imports

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

myapp_obj = Flask(__name__)

#Required when using Flask forms
basedir = os.path.abspath(os.path.dirname(__file__))

#Some configuration for Flask & SQLAlchemy
myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),   #Setup location for app.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
)

#Init db and bcrypt
db = SQLAlchemy(myapp_obj)
bcrypt = Bcrypt(myapp_obj)

#Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(myapp_obj)

from app import routes  #The routes get imported below the Flask() object call
from app import models

