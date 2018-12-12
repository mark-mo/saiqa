import mysql.connector
from mysql.connector import errorcode

# Created by: Mark Mott
# A super class for creating a connection to the database
class Connection:
    def connect(self):
        try:#Initial Catalog=Sima;User Id=markm;Password=Steven2401
            # Connect to a localhost database
            self.cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='saiqa')
            # Connect to a Azure database
            #self.cnx = mysql.connector.connect(user='root', password='root',
                              #host='localhost',
                              #database='saiqa')
            self.cur = self.cnx.cursor()
        except mysql.connector.Error as err: # An error has occured when connecting to the database
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # TODO: Throw the error so it is caught higher up
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # TODO: Throw the error so it is caught higher up
                print("Database does not exist")
            else: # If the error does not match the two known errors, just print out the error
                # TODO: Throw the error so it is caught higher up
                print(err)