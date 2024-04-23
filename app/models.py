from app import db
from app import login_manager
from app import bcrypt
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(60), nullable=False)
    lname = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(60), nullable=False)
    user_attributes = db.relationship('UserAttributes', backref='user', lazy=True)

    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def getID(self):
        return self.id

class UserAttributes(db.Model, UserMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(50))  # Role of the user (e.g., librarian, regular user)
    department = db.Column(db.String(100))  # Department the user belongs to (if applicable)
    fees = db.Column(db.Float, default=0.0)  # Current fees user owes
    member_status = db.Column(db.String(30), default="")
    can_order_books = db.Column(db.Boolean, default=False)  # Whether the user can order books
    can_manage_fines = db.Column(db.Boolean, default=False)  # Whether the user can 
    can_modify_catalog = db.Column(db.Boolean, default=False) #Whether the user can add/remove books in catalog
    can_modify_accounts = db.Column(db.Boolean, default=False) #Whether the user can add/delete accounts for whatever reason (admin)

class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    book_attributes = db.relationship('BookAttributes', backref='book', lazy=True)

class BookAttributes(db.Model, UserMixin):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    genre = db.Column(db.String(100))  # Department the user belongs to (if applicable)
    stock_quantity = db.Column(db.Float, default=0.0)  # Current fees user owes
    is_available = db.Column(db.Boolean, default=False)  # Whether the user can order books

def initializeDB():
    adminExists = bool(User.query.filter_by(email="admin@gmail.com").first()) 
    if (~adminExists):  #If the admin doesn't exist then the db never initialized
        
        #Insert admin with admin privileges
        new_user = User(email="admin@gmail.com")
        new_user.set_password("password123")
        db.session.add(new_user)
        db.session.commit()
        new_user_attr = UserAttributes(user_id=new_user.getID(), role="Admin", department="Administration", can_manage_fines=True)
        #Change attributes                                     
        db.session.add(new_user_attr)
        db.session.commit()
        #Insert librarian with some privileges

        #Insert some test users with base privileges   

        #Initialize sample books & attributes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))