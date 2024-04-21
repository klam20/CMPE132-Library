#__init__.py lets Python know that all files in same directory can be accessed in imports

from flask import Flask
myapp_obj = Flask(__name__)

from app import routes  #The routes get imported below the Flask() object call

#Required when using forms
myapp_obj.config.from_mapping(  
    SECRET_KEY = 'blahblahblah',
)