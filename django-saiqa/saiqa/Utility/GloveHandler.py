import urllib
import os

from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import Text8Corpus
from gensim.similarities.index import AnnoyIndexer

class GloveHandler:
    model = ''
    
    def __init__(self):
        # Set up the model and vector that we are using in the comparison
        self.model = Word2Vec.load(os.getcwd() + "\\saidj\\weights\\mrvec.model")
    
    # Returns the nth closest word to the current one
    def findnearest(self, word, n):
        # 100 trees are being used in this example
        annoy_index = AnnoyIndexer(self.model, 100)
        # Derive the vector for the word "science" in our model
        vector = self.model[word]
        # The instance of AnnoyIndexer we just created is passed 
        approximate_neighbors = self.model.most_similar([vector], topn=11, indexer=annoy_index)
        # Return the neighbor to the specified distance
        return approximate_neighbors[n][0]
