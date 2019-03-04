# Handles calls to the user database.  Subclass of Connection so the logic to connect to the database only is in one place
# Created by Mark Mott
from .ConnectionDAO import Connection
from saiqa.Exception.CustomException import DuplicateUserError

# Data layer for the User Controller
class UserDAO(Connection):
    # Ensures that the superclass is initialized
    def __init__(self):
        super().__init__()
    
    # Logic to create a unique user
    def createUser(self,user):
        # Compare user to database
        self.connect() # Create database connection using the superclass
        try:
            values = [ user.getusername(), user.getpassword() ] # Array allows for cleaner database calls
            selectQuery = 'SELECT * FROM user WHERE u_name = %s AND u_password = %s'
            self.cur.execute(selectQuery,values)
            result = self.cur.fetchall() # Get the result of the query
            # If the database finds anything, throw an error
            if len(result) == 1:
                raise DuplicateUserError
            # Create a new user if it does not exist
            values.append(user.getpermission())
            insertQuery = 'INSERT INTO user (`u_name`, `u_password`,`u_permission`) VALUES (%s,%s,%s)'
            self.cur.execute(insertQuery,values)
            self.cnx.commit()
            id = self.cur.lastrowid # Gets the id of the newly created user.  For testing only
        except DuplicateUserError:
            print('User already exists')
            return False
        finally:
            # Close database connection
            self.cur.close()
            self.cnx.close()
        return True
        
    # Logic to find a user
    def findUser(self,user):
        # Compare user to database
        self.connect() # Create database connection using the superclass
        values = [ user.getusername(), user.getpassword() ] # Array allows for cleaner database calls
        selectQuery = 'SELECT * FROM user WHERE u_name = %s AND u_password = %s'
        self.cur.execute(selectQuery,values)
        result = self.cur.fetchall() # Get the result of the query
        
        # Close the connection to the database
        self.cur.close()
        self.cnx.close()
        # If the database finds anything, create a user
        if len(result) == 1:
            return result[0][3]
        else:
            return -1 # Switch to raising an error
        
    # Logic to find the permission level of a user
    def findPermissions(self,user):
        # Compare user to database
        self.connect()
        values = [ user.getusername(), user.getpassword() ] # Array allows for cleaner database calls
        selectQuery = ("SELECT u_permission FROM user WHERE u_name = %s AND u_password = %s")
        self.cur.execute(selectQuery,values)
        user.setPermission(result)
        return user # Returns user with correct permissions