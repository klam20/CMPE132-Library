#Where the routing of the webpage occurs
from app import myapp_obj, db
from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from .forms import RegistrationForm
from .forms import LoginForm
from .models import *

#Default Redirect to home
@myapp_obj.route("/")
def index():
    return redirect('/home')

#Home page
@myapp_obj.route("/home", methods=['GET','POST'])
def home():
    form = LoginForm()                                                    
    if current_user.is_authenticated:                                     #Check if logged in, display an HTML specifically
        if request.method == 'POST':                                      #for logged in user
            if request.form.get('logOut') == 'Log-Out':                     
                logout_user()
                return redirect('/home')
        return render_template('home_logged_in.html', form=form)
    
    else:                                                                 #Likewise an HTML for logged-out user is used
        if request.method == 'POST':                                     
            if request.form.get('logIn') == 'Log-In': 
                return redirect('/login')
            elif request.form.get('signUp') == 'Sign-Up':
                return redirect('/register')
        return render_template('home_logged_out.html', form=form)

#Login Page
@myapp_obj.route("/login", methods=['GET','POST'])
def login():    
    form = LoginForm()
    if form.validate_on_submit():                                                           #If Login Form submit is pressed
        emailExists = bool(User.query.filter_by(email=form.email.data).first())                 #Check if email exists
        if (emailExists):                                                                   
            user = User.query.filter_by(email = form.email.data).first()                        #Query DB
            if (user.check_password(form.password.data)):                                       #Check if form PW matches DB password
                login_user(user)
                return redirect('/home')
            else:
                flash(f'Invalid password')
        else:                                                                               #Else email does not exist
            flash(f'Account does not exist')
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
            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)                                              
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")


    return render_template('register.html', form=form)