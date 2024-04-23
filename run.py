#Just runs the overall project using > python3 run.py
from app import myapp_obj
from app import db

with myapp_obj.app_context():
    db.create_all()

myapp_obj.run(debug=True)


