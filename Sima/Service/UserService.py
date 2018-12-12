from Sima.Model.UserModel import User
from Sima.DAO.UserDAO import UserDAO

class UserService(object):
    def __init__(self):
        self.data = UserDAO()
        
    def createUser(self,user):
        return self.data.createUser(user)
    
    def findUser(self,user):
        return self.data.findUser(user)