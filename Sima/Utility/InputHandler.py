import regex as re
import nltk
from Sima.Model.Sentence import Sentence
# ,\n|,$|\.\n|\(.*?\)|\[.*?\]|(?<! [A-Z].)\.

class InputHandler():
    def cleanUp(self, input):
        hold = []
        for line in conLines:
            reg = ',\n|,$|\.\n|\(.*?\)|\[.*?\]|(?<! [A-Z].)\.'
            s = re.sub(reg,'',line)
            hold.append(s)
            
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