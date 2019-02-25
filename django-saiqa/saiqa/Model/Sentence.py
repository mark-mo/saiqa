# A base sentence model for storing information related to sentences
# Created by: Mark Mott
class Sentence:
    # A single underline denotes a private method/variable.
    # Default is the property category
    def __init__(self, sentence, subject, category='Property'):
        self.setsentence(sentence)
        self.setsubject(subject)
        self.setcategory(category)
        
    def setsentence(self,sentence):
        self._sentence = sentence
    
    def getsentence(self):
        return self._sentence
        
    def setsubject(self,subject):
        self._subject = subject
    
    def getsubject(self):
        return self._subject
    
    def setcategory(self,category):
        self._category = category
    
    def getcategory(self):
        return self._category
    
    # Allows for Sentence models to better be turned into json
    def toString(self):
        out = {
            "sentence": self.getsentence(),
            "subject": self.getsubject(),
            "category": self.getcategory()
        }
        return out