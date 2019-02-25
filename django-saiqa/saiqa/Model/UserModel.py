# A simple User model for logging in/registering
# Created by: Mark Mott
class User:
    # A single underline denotes a private method/variable.
    # Default is a Guest user
    def __init__(self, username='Guest', password='guest', permission=0):
        print(username)
        self.username = username
        self.password = password
        self.permission = permission
        
    def setusername(self,username):
        self.username = username
    
    def getusername(self):
        return self.username
        
    def setpassword(self,password):
        self.password = password
    
    def getpassword(self):
        return self.password
    
    def setpermission(self,permission):
        self.permission = permission
    
    def getpermission(self):
        return self.permission
    
    def toString(self):
        out = {
            "username": self.getusername(),
            "password": self.getpassword(),
            "permission": self.getpermission()
        }
        return out