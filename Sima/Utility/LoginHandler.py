from flask import session

class LoginHandler:
    def loggedIn(self, f):
        if 'user' in session:
            self.f()
        else:
            redirect(url_for('/'))