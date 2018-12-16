# Handles data meant to be learned from or questions.
# Created by Mark Mott
import regex as re
import nltk
from Sima.Model.Sentence import Sentence

class InputHandler():
    # Removes unwanted noise from the input
    def cleanUp(self, input):
        hold = []
        for line in conLines:
            reg = ',\n|,$|\.\n|\(.*?\)|\[.*?\]|(?<! [A-Z].)\.' # Regex pattern for most unwanted cases
            s = re.sub(reg,'',line)
            hold.append(s)
        return hold
    
    # Turns input into a form the database can accept
    def storeInput(input):
        lem = []
        pos = []
        sub = []
        
        # Seperate input into sentences
        # Lemmatize input
        # Store input into Sentence objects by their subjects
        # return list of objects
    
    # Lemmatizes the input
    def lemInput(input):
        lem = []
        pos = []
        sub = []
        
        text = nltk.word_tokenize(input)
        # Lemmatize all words
        for word in text:
            lem.append(wordnet_lemmatizer.lemmatize(word))
        # Attach POS to all words
        pos = nltk.pos_tag(text)
        
        # Store Subjects in a list
        for word in pos:
            
        
        # If subject is indefinite, make it the previous subject
        
        # Return list of lemmatized sentences and subjects