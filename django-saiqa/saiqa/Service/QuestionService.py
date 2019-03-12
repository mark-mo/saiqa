#A simple service for answering questions and storing sentences.  Currently only an inbetween class.
# Created by Mark Mott
from saiqa.DAO.QuestionDAO import QuestionDAO

print('QuestionS')

class QuestionService(object):
    def __init__(self):
        self.data = QuestionDAO() # Creates an instance of the UserDAO class
    
    
    # Passes list of Sentences to createSents in QuestionDAO
    def createSents(self, sents, ref, trust):
        return self.data.createSents(sents, ref, trust)
    
    
    # Passes a subject and a category to findUser in UserDAO
    def findbysubject(self, sub, cat, user):
        # Get sentences
        if self.data.updatesubject(sub, user):
            return self.data.findbysubject(sub, cat)
        else:
            return ['Nothing', '']
    
    
    # Gets a random fact of the most searched subject
    def findbyfrequent(self, user):
        return self.data.findbyfrequent(user)
    
    
    # Gets a random fact from the database
    def findByRandom(self):
        # Get a random sentence
        return self.data.findbyrandom()
    