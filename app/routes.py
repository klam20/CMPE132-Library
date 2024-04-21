from app import myapp_obj
from flask import render_template
from forms import RegistrationForm
from forms import LoginForm

@myapp_obj.route("/")
def index():
    return render_template('index.html')

@myapp_obj.route("/login", methods=['GET','POST'])
def login():    
    form = LoginForm()
    if form.validate_on_submit():  #If Login Form submit is pressed
        return "<p>10101</p>"
        #Check if email exists against db
        #If exists                                                                   
            #Check password
                #If PW GOOD LOGIN (AUTHENTICATE)
                #ELSE RETRY
    return render_template('login.html', form=form)

@myapp_obj.route("/register", methods=['GET','POST'])
def register():    
    form = RegistrationForm()
    if form.validate_on_submit():  #If Login Form submit is pressed
        return "<p>10101</p>"
        #Check if email exists against db
        #If exists send msg
        #Else continue                                                             
    return render_template('register.html', form=form)