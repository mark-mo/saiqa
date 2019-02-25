# Handles connecting to the database.  Superclass of all other classes on the data layer
# Created by Mark Mott
import mysql.connector
from mysql.connector import errorcode

# Created by: Mark Mott
# A super class for creating a connection to the database
class Connection:
    def connect(self):
        try:
            # Connect to a localhost database
            self.cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='saiqa')
            # Connect to a Azure database
            #self.cnx = mysql.connector.connect(user='root', password='root',
                              #host='localhost',
                              #database='saiqa')
            self.cur = self.cnx.cursor() # This object is what queries are made with
        except mysql.connector.Error as err: # An error has occured when connecting to the database
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # TODO: Throw the error so it is caught higher up
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # TODO: Throw the error so it is caught higher up
                print("Database does not exist")
            else: # If the error does not match the two known errors, just print out the error
                # TODO: Change to throw custom exception
                print(err)