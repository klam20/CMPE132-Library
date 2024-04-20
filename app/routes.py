from app import myapp_obj

@myapp_obj.route("/")
def hello_world():
    return "<p>Hello, World!</p>"