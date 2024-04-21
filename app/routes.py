#Where the routing of the webpage occurs
from app import myapp_obj, db
from flask import render_template, request, redirect, session, flash
from .forms import RegistrationForm
from .forms import LoginForm
from .models import User

#Default Page
@myapp_obj.route("/")
def index():
    return render_template('index.html')

#Login Page
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

#Register Page
@myapp_obj.route("/register", methods=['GET','POST'])
def register():    
    form = RegistrationForm()
    if form.validate_on_submit():  #If Register Form submit is pressed
        emailExists = bool(User.query.filter_by(email=form.email.data).first())  #If Email Exists
        if emailExists:
            flash(f'Account already exists')
            return redirect("/register")
        else:
            new_user = User(email=form.email.data, password=form.password.data)                                              #Register then
            db.session.add(new_user)
            db.session.commit()


    return render_template('register.html', form=form)