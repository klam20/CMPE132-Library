#__init__.py lets Python know that all files in same directory can be accessed in imports

from flask import Flask
myapp_obj = Flask(__name__)

from app import routes