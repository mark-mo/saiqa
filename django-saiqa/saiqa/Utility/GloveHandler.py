import urllib
import os

from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import Text8Corpus
from gensim.similarities.index import AnnoyIndexer

from saiqa.Utility.LoggingDecorator import *

# Handles logging.
logging = Loggingdec()

class GloveHandler:
    def __init__(self):
        # Set up the model and vector that we are using in the comparison
        self.model = Word2Vec.load(os.getcwd() + "\\saidj\\weights\\mrvec.model")
    
    # Returns the closest three words to the current one
    def findnearest(self, word): # TODO: Add a try catch
        try:
            logging.entry("LoginController.reguser")
            # 100 trees are being used in this example
            annoy_index = AnnoyIndexer(self.model, 100)
            # Derive the vector for the word "science" in our model
            vector = self.model[word]
            # The instance of AnnoyIndexer we just created is passed 
            approximate_neighbors = self.model.most_similar([vector], topn=11, indexer=annoy_index)
            # Return the neighbor to the specified distance
            return approximate_neighbors[1:3][0]
        except KeyError as error:
            logging.error(error)
            return ['-','-','-']
