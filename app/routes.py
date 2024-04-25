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
    # Check if user is authenticated
    if current_user.is_authenticated:
        user_permissions = Permissions.query.filter_by(role=current_user.role).first()
        can_view_book_backlog = user_permissions.can_view_book_backlog if user_permissions else False
        can_view_accounts = user_permissions.can_view_accounts if user_permissions else False
        can_request_checkout = user_permissions.can_request_checkout if user_permissions else False
        can_approve_checkout = user_permissions.can_approve_checkout if user_permissions else False
        can_modify_catalog = user_permissions.can_modify_catalog if user_permissions else False
        can_modify_accounts = user_permissions.can_modify_accounts if user_permissions else False

        if request.method == 'POST':                                      #for logged in user
            if request.form.get('logOut') == 'Log-Out':                     
                logout_user()
                return redirect('/home')

        return render_template('home_logged_in.html', 
                               can_view_book_backlog=can_view_book_backlog,
                               can_view_accounts=can_view_accounts,
                               can_request_checkout=can_request_checkout,
                               can_approve_checkout=can_approve_checkout,
                               can_modify_catalog=can_modify_catalog,
                               can_modify_accounts=can_modify_accounts,
                               role=current_user.role
                               )
    
    else:                                                                 #Likewise an HTML for logged-out user is used
        if request.method == 'POST':                                     
            if request.form.get('logIn') == 'Log-In': 
                return redirect('/login')
            elif request.form.get('signUp') == 'Sign-Up':
                return redirect('/register')
        return render_template('home_logged_out.html')

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
        return render_template('browse_books_logged_in.html', title='Catalog', bookCount=bookCount, books=books, role=current_user.role)

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
                if (attributes.stock_quantity > 0):
                    flash(f'You borrowed one book, check your log for approval')
                    #Update stock
                    attributes.stock_quantity = attributes.stock_quantity - 1

                    #Update user back log
                    new_userbook = UserBooks(user_id=current_user.id, book_id=book_id, approved=False)

                    #Update library back log
                    new_backlog = CheckoutApproval(user_id=current_user.id, book_id=book_id, approved_by_librarian=False, approved_by_assistant=False)
                    
                    #Add & Commit
                    db.session.add(new_userbook)
                    db.session.add(new_backlog)
                    db.session.commit()

                else:
                    flash(f'Sorry! Out of stock')
                return redirect('/browse_books/' + str(book_id))
        return render_template('view_book_logged_in.html', title='Catalog', book=book, attributes=attributes, role = current_user.role)
    else:
        if request.method == 'POST':                                      
            if request.form.get('Borrow') == 'Borrow': 
                flash(f'Must be logged in')
                return redirect('/login')

        return render_template('view_book_logged_out.html', title='Catalog', book=book, attributes=attributes)

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
    
@myapp_obj.route('/view_book_backlog', methods=['GET'])
def book_backlog():
    #Obtain the book backlog using userBooks
    backlog_count = CheckoutApproval.query.count()
    checkout_backlog = CheckoutApproval.query.all()
    return render_template('view_book_backlog.html', title='Book Backlog', role=current_user.role, backlog=checkout_backlog, count=backlog_count)


@myapp_obj.route('/view_delete_backlog', methods=['GET'])
def delete_backlog():
    return render_template('view_delete_backlog.html', title='Delete Backlog', role=current_user.role)


@myapp_obj.route('/manage_books', methods=['GET'])
def manage_books():            
    return render_template('manage_books.html', title='Manage Books', role=current_user.role)

