from models import *

def determineAccessToBook(user, bookId):
    # Define RBAC policy rules
    
    # If user is admin, grant full access
    if user.role == "Admin":
        return True

    # If user is a librarian and object is a book, grant access to manage book attributes
    if user.role in ("Librarian", "Library Assistant", "Admin"):
        return True
    
    # If user is a regular user and object is a book, grant access to view book details
    if user.role in ("Student", "Teacher"):
        return True

    # If user is a regular user and object is not a book, deny access
    if user.role == "Guest":
        return False

    # Default deny
    return False

