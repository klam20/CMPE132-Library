from app import db
from app import login_manager
from app import bcrypt
from app import basedir, os
from datetime import datetime
from flask_login import UserMixin
import csv
import string

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(60), nullable=True)
    lname = db.Column(db.String(60), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(50))  # Role of the user (e.g., librarian, regular user)
    owns_num_books = db.Column(db.Integer, default = 0, nullable=True) #How many books they own
    owned_books = db.relationship('UserBooks', backref='user', lazy=True)

    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class CheckoutApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    approver = db.Column(db.String(50), default="n/a")
    decision = db.Column(db.String(25), default="Pending")


class UserDeletionApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approved_by_admin = db.Column(db.Boolean, default=False)
    approved_by_librarian = db.Column(db.Boolean, default=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    synopsis = db.Column(db.String(500), nullable=True)
    
    book_attributes = db.relationship('BookAttributes', backref='book', lazy=True)
    owned_by_users = db.relationship('UserBooks', backref='book', lazy=True)


class BookAttributes(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    genre = db.Column(db.String(100))  # Department the user belongs to (if applicable)
    stock_quantity = db.Column(db.Integer, default=0.0)  # Current fees user owes
    is_available = db.Column(db.Boolean, default=False)  # Whether the book is reserved for a high priority reason (like for a classroom let's say)

class UserBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    approved = db.Column(db.String(25), default=False)  #Can be ["Pending", "Denied", "Approved", "Returned"]
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True) 
    # Additional attributes specific to the user-book relationship can be added here if needed

class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)

    #Role based permissions for page access
    can_view_book_backlog = db.Column(db.Boolean, default=False)    #Admin/Librarian/LibraryStaff
    can_view_accounts = db.Column(db.Boolean, default=False)    #Admin only

    #Button permissions
    can_request_checkout = db.Column(db.Boolean, default=False)    #Making a request to checkout a book that is later approved (students,teachers)
    can_approve_checkout = db.Column(db.Boolean, default=False)    #Adding book checkout to official db     (librarian/librarystaff)
    can_modify_catalog = db.Column(db.Boolean, default=False)   #Adding/removing from catalog               (typically admin/librarian/librarystaff)
    can_modify_accounts = db.Column(db.Boolean, default=False)  #Adding/removing account manually into db   (typically admin only)

    # Additional attributes specific to the user-book relationship can be added here if needed

def checkPermission(role, permission_name):
    getRole = Permissions.query.filter_by(role=str(role)).first()
    return bool(getattr(getRole, permission_name))    #Should return a bool

def initializeDB():
    if not db.session.query(User).filter_by(email="admin@gmail.com").first():        #Insert admin with admin privileges
        new_user = User(email="admin@gmail.com", role="Admin")
        new_user.set_password("123")
        db.session.add(new_user)
        db.session.commit()
     
        #Insert librarian with some privileges
        new_user = User(email="library@gmail.com", role="Librarian")
        new_user.set_password("123")
        db.session.add(new_user)
        db.session.commit()
        #Insert library assistant with some privileges
        new_user = User(email="assistant@gmail.com", role="Library Assistant")
        new_user.set_password("123")
        db.session.add(new_user)
        db.session.commit()
        
        #Insert student user with base privileges   
        new_user = User(email="student@gmail.com", role="Student")
        new_user.set_password("123")
        db.session.add(new_user)
        db.session.commit()

        #Insert a requested book by a user
        new_checkout = UserBooks(user_id=1, book_id=1, approved=False)
        db.session.add(new_checkout)
        db.session.commit()

        #Insert a book request
        new_checkout = CheckoutApproval(user_id=1, book_id=1)
        db.session.add(new_checkout)
        db.session.commit()

        #Initialize role permissions
        temp_perm = Permissions (
            #Role based permissions for page access
            role = "Admin",
            can_view_book_backlog = True,
            can_view_accounts = True,

            #Button permissions
            can_request_checkout = True,
            can_approve_checkout = True,
            can_modify_catalog = True,
            can_modify_accounts = True,
        )
        db.session.add(temp_perm)

        temp_perm = Permissions (
            #Role based permissions for page access
            role = "Librarian",
            can_view_book_backlog = True,
            can_view_accounts = False,

            #Button permissions
            can_request_checkout = True,
            can_approve_checkout = True,
            can_modify_catalog = True,
            can_modify_accounts = False,
        )
        db.session.add(temp_perm)

        temp_perm = Permissions (
            #Role based permissions for page access
            role = "Library Assistant",
            can_view_book_backlog = True,
            can_view_accounts = False,

            #Button permissions
            can_request_checkout = True,
            can_approve_checkout = True,
            can_modify_catalog = False,
            can_modify_accounts = False,
        )
        db.session.add(temp_perm)

        temp_perm = Permissions (
            #Role based permissions for page access
            role = "Student",
            can_view_book_backlog = True,
            can_view_accounts = False,

            #Button permissions
            can_request_checkout = True,
            can_approve_checkout = True,
            can_modify_catalog = False,
            can_modify_accounts = False,
        )
        db.session.add(temp_perm)

        temp_perm = Permissions (
            #Role based permissions for page access
            role = "Teacher",
            can_view_book_backlog = True,
            can_view_accounts = False,

            #Button permissions
            can_request_checkout = True,
            can_approve_checkout = True,
            can_modify_catalog = False,
            can_modify_accounts = False,
        )
        db.session.add(temp_perm)

        db.session.commit()

def initializeBooks():
        with open(os.path.join(basedir, 'static/books/books.csv'), 'r') as file:
            reader = csv.DictReader(file)
            for sample_book_details in reader:
                # Check if the book already exists
                if not Book.query.filter_by(name=sample_book_details["name"]).first():
                    # Create the book
                    sample_book = Book(
                        name=sample_book_details["name"],
                        author=sample_book_details["author"],
                        synopsis=sample_book_details["synopsis"]
                    )

                    # Add the book to the session and commit changes to the database
                    db.session.add(sample_book)
                    db.session.commit()

                    # Create attributes for the book
                    sample_book_attributes = BookAttributes(
                        book_id=sample_book.id,
                        genre=sample_book_details["genre"],
                        stock_quantity=float(sample_book_details["stock_quantity"]),  # Convert to float if necessary
                        is_available=bool(sample_book_details["is_available"])  # Convert to bool if necessary
                    )

                    # Add the book attributes to the session and commit changes to the database
                    db.session.add(sample_book_attributes)
                    db.session.commit()

def getUserBook(input):
    id, user_id, book_id = input.split(',')    #Use , delimiter to split string
    return (id.strip(), user_id.strip(), book_id.strip())   #.strip() removes extra whitespace/trailing


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))