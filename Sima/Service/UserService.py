#A simple service for login and register.  Currently only an inbetween class.
# Created by Mark Mott
from Sima.Model.UserModel import User
from Sima.DAO.UserDAO import UserDAO

class UserService(object):
    def __init__(self):
        self.data = UserDAO() # Creates an instance of the UserDAO class
        
    # Passes a user to createUser in UserDAO
    def createUser(self,user):
        return self.data.createUser(user)
    
    # Passes a user to findUser in UserDAO
    def findUser(self,user):
        # Add correct permission level to user
        return self.data.findUser(user)