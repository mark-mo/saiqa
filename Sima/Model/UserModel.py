# A simple User model for logging in/registering
# Created by: Mark Mott
class User:
    # A single underline denotes a private method/variable.
    # Default is a Guest user
    def __init__(self, username='Guest', password='guest', permission=0):
        print(username)
        self.setUsername(username)
        self.setPassword(password)
        self.setPermission(permission)
        
    def setUsername(self,username):
        self._username = username
    
    def getUsername(self):
        return self._username
        
    def setPassword(self,password):
        self._password = password
    
    def getPassword(self):
        return self._password
    
    def setPermission(self,permission):
        self._permission = permission
    
    def getPermission(self):
        return self._permission
    
    def toString(self):
        out = {
            "username": self.getUsername(),
            "password": self.getPassword(),
            "permission": self.getPermission()
        }
        return out