# Handles creating and destroying a test database.  Subclass of Connection so the logic to connect to the database only is in one place
# Created by Mark Mott
from .ConnectionDAO import Connection

class TestDAO(Connection):
    # Ensures that the superclass is initialized
    def __init__(self):
        super().__init__()
    
    # Create a test database
    def createData(self):
        # Create the test database
        self.connect('none') # Create database connection using the superclass
        self.cur.execute("CREATE DATABASE simatest")
        # Populate the database with tables
        self.cur.execute("CREATE TABLE simatest.user SELECT * FROM saiqa.user WHERE 1=0")
        self.cur.execute("CREATE TABLE simatest.reference SELECT * FROM saiqa.reference WHERE 1=0")
        self.cur.execute("CREATE TABLE simatest.data SELECT * FROM saiqa.data WHERE 1=0")
        self.cur.execute("CREATE TABLE simatest.userdata SELECT * FROM saiqa.userdata WHERE 1=0")
        self.cur.close()
    
    # Destroy the test database
    def destroyData(self):
        self.connect('none')
        self.cur.execute("DROP DATABASE simatest")