from Sima.DAO.ConnectionDAO import Connection

class UserDAO(Connection):
    def __init__(self):
        super().__init__()
        
    def createUser(self,user):
        # Compare user to database
        self.connect()
        values = [ user.getUsername(), user.getPassword(), user.getPermission() ]
        selectQuery = 'SELECT * FROM user WHERE u_name = %s AND u_password = %s AND u_permission = %s'
        self.cur.execute(selectQuery,values)
        result = self.cur.fetchall()
        # If the database finds anything, throw an error
        print(len(result))
        if len(result) == 1:
            return False # Switch to raising an error
        # Create a new user
        insertQuery = 'INSERT INTO user (`u_name`, `u_password`,`u_permission`) VALUES (%s,%s,%s)'
        self.cur.execute(insertQuery,values)
        self.cnx.commit()
        id = self.cur.lastrowid
        print(id)
        self.cur.close()
        self.cnx.close()
        return True
        
    def findUser(self,user):
        # Compare user to database
        self.connect()
        values = [ user.getUsername(), user.getPassword() ]
        selectQuery = 'SELECT * FROM user WHERE u_name = %s AND u_password = %s'
        self.cur.execute(selectQuery,values)
        result = self.cur.fetchall()
        # If the database finds anything, create a user
        print(result)
        if len(result) == 1:
            self.cur.close()
            self.cnx.close()
            return True
        else:
            self.cur.close()
            self.cnx.close()
            return False # Switch to raising an error
        
    def findPermissions(self,user):
        # Compare user to database
        self.connect()
        values = [ user.getUsername(), user.getPassword() ]
        selectQuery = ("SELECT u_permission FROM user WHERE u_name = %s AND u_password = %s")
        self.cur.execute(selectQuery,values)
        print(result) # Test line, DELETE when done
        user.setPermission(result)
        return user