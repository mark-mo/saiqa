# Not yet implemented
# Created by Mark Mott
from flask import session

# A decorator to handle if the user can access a method or not
class LoginHandler:
    def loggedIn(self, f):
        if 'user' in session:
            self.f() # Runs the method if the user is in the session
        else:
            redirect(url_for('/')) # Redirects to home if a user is not in the session