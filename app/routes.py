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
    initializeDB()
    initializeBooks()
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

@myapp_obj.route("/browse_books", methods=['GET','POST'])
def library():    
    #Fetch books from db
    bookCount = Book.query.count()
    books = Book.query.all()
    if current_user.is_authenticated:
        return render_template('browse_books_logged_in.html', title='Catalog', bookCount=bookCount, books=books)
    else:
        return render_template('browse_books_logged_out.html', title='Catalog', bookCount=bookCount, books=books)

@myapp_obj.route('/browse_books/<int:book_id>', methods=['GET','POST'])        #URL varies to view different email messages
def bookView(book_id):    
    #Fetch books from db
    book = Book.query.filter_by(id=book_id).first()
    attributes = BookAttributes.query.filter_by(book_id=book_id).first()
    if current_user.is_authenticated:
        #Attempt to borrow book
        if request.method == 'POST':                                      
            if request.form.get('Borrow') == 'Borrow': 
                #Check policy       
                flash(f'Hello1')
                return redirect('/browse_books/' + str(book_id))
        return render_template('view_book_logged_in.html', title='Catalog', book=book, attributes=attributes)
    else:
        if request.method == 'POST':                                      
            if request.form.get('Borrow') == 'Borrow': 
                #Check policy   
                flash(f'Hello2')
                return redirect('/browse_books/' + str(book_id))

        return render_template('view_book_logged_out.html', title='Catalog', book=book, attributes=attributes)

@myapp_obj.route("/manage_account", methods=['GET','POST'])
def manageacc():
    return render_template('manage_account.html', title='Manage Account')

@myapp_obj.route('/search_book', methods=['GET'])
def search_book():
    query = request.args.get('query')
    if query:
        results = Book.query.filter(
            Book.name.ilike(f"%{query}%") |
            Book.author.ilike(f"%{query}%") | 
            Book.synopsis.ilike(f"%{query}%"))
        bookCount = results.count()
        if current_user.is_authenticated:
            return render_template('browse_books_logged_in.html', title='Catalog', bookCount=bookCount, books=results.all())
        else:
            return render_template('browse_books_logged_out.html', title='Catalog', bookCount=bookCount, books=results.all())
    
    