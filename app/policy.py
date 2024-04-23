from models import *

def determineAccess(user, obj):
    # Get user attributes
    user_attributes = UserAttributes.query.filter_by(user_id=user.id).first()
    object_attributes = BookAttributes.query.filter_by(book_id=obj.id).first()

    # Define your ABAC policy rules
    
    # If user is admin, grant full access
    if user_attributes.role == "Admin":
        return True

    # If user is a librarian and object is a book, grant access to manage book attributes
    if user_attributes.role == "Librarian":
        return True

    # If user is a regular user and object is a book, grant access to view book details
    if user_attributes.role == "Student":
        return True

    # If user is a regular user and object is not a book, deny access
    if user_attributes.role == "Guest":
        return False

    # Default deny
    return False