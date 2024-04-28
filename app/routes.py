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
    initializeDB()      #Runs one time, afterwards it is blocked
    initializeBooks()
    #showEncryptedPasswords()    #Shows encrypted passwords of all accounts just for learning purposes, should be removed in general
    # Check if user is authenticated
    if current_user.is_authenticated:
        user_permissions = Permissions.query.filter_by(role=current_user.role).first()
        can_view_book_backlog = user_permissions.can_view_book_backlog
        can_view_accounts = user_permissions.can_view_accounts

        if request.method == 'POST':                                      #for logged in user
            if request.form.get('logOut') == 'Log-Out':                     
                logout_user()
                return redirect('/home')
            
            elif request.form.get('Delete') == 'Delete':
                getUser = User.query.filter_by(id=current_user.id).first()
                getUser.user_request_delete = True
                db.session.add(getUser)
                db.session.commit()

        return render_template('home_logged_in.html', 
                               can_view_book_backlog=can_view_book_backlog,
                               can_view_accounts=can_view_accounts
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
            new_user = User(email=form.email.data, role="Student", fname=form.fname.data, lname=form.lname.data)
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
        user_permissions = Permissions.query.filter_by(role=current_user.role).first()
        can_view_book_backlog = user_permissions.can_view_book_backlog
        can_view_accounts = user_permissions.can_view_accounts
        can_modify_catalog = user_permissions.can_modify_catalog

                
        return render_template('browse_books_logged_in.html', title='Catalog', bookCount=bookCount,
                                books=books, can_view_book_backlog=can_view_book_backlog,
                                can_view_accounts=can_view_accounts, can_modify_catalog=can_modify_catalog)

    else:
        return render_template('browse_books_logged_out.html', title='Catalog', bookCount=bookCount, books=books)

@myapp_obj.route("/modify_catalog", methods=['POST'])
def modifycatalog():
    user_permissions = Permissions.query.filter_by(role=current_user.role).first()
    if request.method == "POST":
        can_modify_catalog = user_permissions.can_modify_catalog
        if (can_modify_catalog):    #Check perm just to be sure
            #Obtain post contents
            bookname = request.form.get('bookname')
            author = request.form.get('author')
            synopsis = request.form.get('synopsis')
            genre = request.form.get('genre')
            stock = request.form.get('stock')
            #Commit the book
            newBook = Book(name=bookname, author=author, synopsis=synopsis)
            db.session.add(newBook)
            db.session.commit()
            #Use book id to add attributes of book
            book = Book.query.filter_by(name=bookname).first()
            bookAttr = BookAttributes(book_id = book.id, genre = genre, stock_quantity=stock)
            #Commit the attributes
            db.session.add(bookAttr)
            db.session.commit()
    return redirect('/browse_books')


@myapp_obj.route('/browse_books/<int:book_id>', methods=['GET','POST'])        #URL varies to view different email messages
def bookView(book_id):  
    #Fetch books from db
    book = Book.query.filter_by(id=book_id).first()
    attributes = BookAttributes.query.filter_by(book_id=book_id).first()
    
    if current_user.is_authenticated:     
        #Attempt to borrow book
        user_permissions = Permissions.query.filter_by(role=current_user.role).first()
        can_view_book_backlog = user_permissions.can_view_book_backlog
        can_view_accounts = user_permissions.can_view_accounts
        can_request_checkout = user_permissions.can_request_checkout

        if request.method == 'POST':                                      
            if request.form.get('Borrow') == 'Borrow':
                if (can_request_checkout == True):        
                    if (attributes.stock_quantity > 0):
                        flash(f'You borrowed one book, check your log for approval')
                        #Update stock
                        attributes.stock_quantity = attributes.stock_quantity - 1

                        #Update user back log
                        new_userbook = UserBooks(user_id=current_user.id, book_id=book_id, approved="Pending")

                        #Update library back log
                        new_backlog = CheckoutApproval(user_id=current_user.id, book_id=book_id)
                        
                        #Add & Commit
                        db.session.add(new_userbook)
                        db.session.add(new_backlog)
                        db.session.commit()

                    else:
                        flash(f'Out of stock')
                else:
                    flash(f'No permission')
                return redirect('/browse_books/' + str(book_id))
        return render_template('view_book_logged_in.html', title='Catalog', book=book,
                                attributes=attributes, can_view_book_backlog=can_view_book_backlog,
                                can_view_accounts=can_view_accounts, )
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
    
@myapp_obj.route('/view_book_backlog', methods=['GET', 'POST'])
def book_backlog():
    user_permissions = Permissions.query.filter_by(role=current_user.role).first()
    can_view_book_backlog = user_permissions.can_view_book_backlog
    can_view_accounts = user_permissions.can_view_accounts
    can_approve_checkout = user_permissions.can_approve_checkout 
    #Obtain the book backlog using userBooks
    backlog_count = CheckoutApproval.query.count()
    checkout_backlog = CheckoutApproval.query.all()

    if request.method == "POST":
        #Obtain the user and book associated through the post request        
        #Checkout query and also set the approver role now
        if (can_approve_checkout == True):

            if request.form.get('approve'):
                #Approve
                id, user_id, book_id = splitFunction(request.form.get('approve')) 
                checkout = CheckoutApproval.query.filter_by(id=id, user_id=user_id, book_id=book_id).first()
                checkout.approver = current_user.role
                
                #UserBooks query
                userBooks = UserBooks.query.filter_by(id=id, user_id=user_id, book_id=book_id).first()

                #Decisions
                checkout.decision = "Approved" 
                checkout.approver = current_user.role
                userBooks.approved = "Approved"
                userBooks.start_time = datetime.now()
                #Do not decrement book stock
                db.session.add(userBooks)
                db.session.add(checkout)
                flash(f'Approved')
            elif request.form.get('deny'):
                #Deny
                id, user_id, book_id = splitFunction(request.form.get('deny')) 

                checkout = CheckoutApproval.query.filter_by(id=id, user_id=user_id, book_id=book_id).first()
                
                #UserBooks query
                userBooks = UserBooks.query.filter_by(id=id, user_id=user_id, book_id=book_id).first()

                #Decisions
                checkout.decision = "Denied"
                checkout.approver = current_user.role

                userBooks.approved = "Denied"

                #Increment book stock back
                incBookStock = (BookAttributes.query.filter_by(book_id=book_id).first())
                incBookStock.stock_quantity = incBookStock.stock_quantity + 1
                db.session.add(userBooks)
                db.session.add(checkout)
                db.session.add(incBookStock)
                flash(f'Deny')
            else: 
                flash(f'Unexpected behavior')
        else:
            flash(f'Cannot approve checkout')

        db.session.commit()

    return render_template('view_book_backlog.html', title='Book Backlog', can_view_accounts=can_view_accounts,
                            can_view_book_backlog=can_view_book_backlog, backlog=checkout_backlog, count=backlog_count)


@myapp_obj.route('/view_delete_backlog', methods=['GET', 'POST'])
def delete_backlog():
    user_permissions = Permissions.query.filter_by(role=current_user.role).first()
    can_view_book_backlog = user_permissions.can_view_book_backlog
    can_view_accounts = user_permissions.can_view_accounts
    can_modify_accounts = user_permissions.can_modify_accounts

    count = User.query.count()
    users = User.query.all()

    
    if request.method == "POST":
        if can_modify_accounts:
            #Check the user's flags if they requested to delete
            id, email, role = splitFunction(request.form.get("Delete"))
            userToDelete = User.query.filter_by(id=id, email=email, role=role).first()
            if userToDelete.user_request_delete:
                #Delete the account from the db
                db.session.delete(userToDelete)
                db.session.commit()
                return(redirect('/view_delete_backlog'))    #Refresh
            else:
                flash(f'Cannot delete without users permission')
        else:
            flash(f'You do not have permission to delete')
    
    return render_template('view_delete_backlog.html', title='Delete Backlog', can_view_accounts=can_view_accounts,
                            can_view_book_backlog=can_view_book_backlog, count=count, users=users)



@myapp_obj.route('/manage_books', methods=['GET', 'POST'])
def manage_books():            
    user_permissions = Permissions.query.filter_by(role=current_user.role).first()
    can_view_book_backlog = user_permissions.can_view_book_backlog
    can_view_accounts = user_permissions.can_view_accounts

    book_count = UserBooks.query.filter_by(user_id=current_user.id).count()
    books = UserBooks.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        if request.form.get('return'):
            id, user_id, book_id = splitFunction(request.form.get('return'))
            returnedBook = UserBooks.query.filter_by(id=id, user_id=user_id, book_id=book_id).first()
            returnedBookStock = BookAttributes.query.filter_by(book_id=book_id).first()
            returnedBook.end_time = datetime.now()
            returnedBook.approved = "Returned"
            returnedBookStock.stock_quantity = returnedBookStock.stock_quantity + 1
            db.session.add(returnedBookStock)
            db.session.add(returnedBook)
            db.session.commit()
            flash(f'Wanted to return book')

    return render_template('manage_books.html', title='Manage Books', can_view_accounts=can_view_accounts,
                            can_view_book_backlog=can_view_book_backlog, count=book_count, books=books)

#Catch all errors that might happen and just go to home page
# @myapp_obj.errorhandler(Exception)
# def page_not_found(error):
#     # Redirect to the home page
#     return redirect('/home')