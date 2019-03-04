# Handles calls to the user database.  Subclass of Connection so the logic to connect to the database only is in one place
# Created by Mark Mott
from .ConnectionDAO import Connection

# Data layer for the User Controller
class QuestionDAO(Connection):
    # Ensures that the superclass is initialized
    def __init__(self):
        super().__init__()

    # Logic to create a unique user
    def createSents(self, sents, ref, rely):
        # Compare user to database
        self.connect()  # Create database connection using the superclass
        # Check if reference already exists
        values = [ref, rely]
        selectQuery = 'SELECT r_id FROM reference WHERE r_fullSource = %s AND r_trust = %s'
        self.cur.execute(selectQuery, values)
        result = self.cur.fetchall()  # Get the result of the query
        # If no results, insert new reference/trust level
        if len(result) == 0:
            insertQuery = 'INSERT INTO reference (`r_fullsource`, `r_trust`) VALUES (%s,%s)'
            self.cur.execute(insertQuery, values)
            self.cnx.commit()
            result = self.cur.lastrowid  # Gets the id of the newly created user
            
        print('Get ready to create')
        for entry in sents:
            # Insert sentence
            subject = ''
            if isinstance(entry.getsubject(), list):
                subject = entry.getsubject()[0]
            else:
                subject = entry.getsubject()
            values = [subject, entry.getsentence(), entry.getcategory(), result]  # Array allows for cleaner database calls
            # Create a new user if it does not exist
            insertQuery = 'INSERT INTO data (`d_subject`, `d_sentence`,`d_category`, `r_id`) VALUES (%s,%s,%s,%s)'
            print(values)
            self.cur.execute(insertQuery, values)
            self.cnx.commit()
        # Close database connection
        self.cur.close()
        self.cnx.close()
        return True

    # Logic to find a list of sentences that match the subject and category
    def findbysubject(self, sub, cat):
        self.connect()  # Create database connection using the superclass
        # Force subject to be a string because of spaCy
        values = [str(sub), cat]  # Array allows for cleaner database calls
        # Get a list of sentences based off of subject and the category
        selectQuery = 'SELECT * FROM data WHERE data.d_subject = %s AND data.d_category = %s'
        print(values)
        self.cur.execute(selectQuery, values)
        results = self.cur.fetchall()  # Get the result of the query
        
        # Close the connection to the database
        self.cur.close()
        self.cnx.close()
        # If the database finds anything, create a list of sentences
        if len(results) > 0:
            return results
        else:
            return ['Nothing', '']  # Switch to raising an error
    
    # Need to test
    def findbyfrequent(self, user):
        self.connect()
        values = [user.getname()]
        
        selectquery = 'SELECT * FROM userdata INNER JOIN user ON userdata.u_id = user.u_id WHERE user.u_name = %s'
        self.cur.execute(selectQuery, values)
        results = self.cur.fetchall()  # Get the result of the query
        
        print(results)
        highest = 0
        for i in range(0, len(results)):
            if highest < results[i]['ud_request']:
                highest = i
        
        print(results[highest])
        values = [results[highest]['d_id']]  # Array allows for cleaner database calls
        # Get a list of sentences based off of subject and the category
        selectQuery = 'SELECT * FROM data WHERE d_id'
        self.cur.execute(selectQuery, values)
        results = self.cur.fetchall()  # Get the result of the query
        
        # Close the connection to the database
        self.cur.close()
        self.cnx.close()
        # If the database finds anything, create a user
        if len(result) > 0:
            return results
        else:
            return ['Nothing', '']  # Switch to raising an error
        
    # Need to test.  Goes to Login and Register
    def findbyrandom(self):
        self.connect()
        selectQuery = 'SELECT * FROM data ORDER BY RAND() LIMIT 1'
        self.cur.execute(selectQuery)
        results = self.cur.fetchall()  # Get the result of the query
        
        return results[0][2]

    # Logic to increment how many times a user looked up a subject
    def updatesubject(self, sub, user):
        self.connect()  # Create database connection using the superclass
        values = [user.getusername(), sub.getsubject()]  # Array allows for cleaner database calls
        # Check if the subject has been search for by the user
        selectquery = 'SELECT ud_request FROM userdata INNER JOIN user ON userdata.u_id = user.u_id INNER JOIN data ON userdata.d_id = data.d_id WHERE user.u_name = %s AND data.d_subject = %s'
        self.cur.execute(selectQuery, values)
        results = self.cur.fetchall()  # Get the result of the query

        # If the subject has been searched for, increment request amount by 1
        if len(results) > 0:
            updateQuery = 'UPDATE userdata INNER JOIN user ON userdata.u_id = user.u_id INNER JOIN data ON userdata.d_id = data.d_id SET ud_request = ud_request + 1 WHERE user.u_name = %s AND data.d_subject = %s'
            self.cur.execute(updateQuery, values)
            results = self.cur.fetchall()  # Get the result of the query
            return true
        # If the subject has not been searched for, create a new entry
        
        # Close the connection to the database
        self.cur.close()
        self.cnx.close()
        # If the database finds anything, create a user
        if len(result) > 0:
            return results
        else:
            return ['Nothing', '']  # Switch to raising an error
