# Handles data meant to be learned from or questions.
# Created by Mark Mott
import regex as re
import json
import nltk
from nltk.parse import CoreNLPDependencyParser

from saiqa.Model.Sentence import Sentence
import saiqa.Training.softmaxR as sr
import spacy


class InputHandler():
    # Removes unwanted noise from the input
    def cleanUp(self, input):
        reg1 = '"'
        fix = re.sub(reg1, '', input)
        reg = '(?<=\.)\n|(?<=[A-z]\.) +(?![A-Z]\.)'  # Regex pattern for most unwanted cases
        s = re.split(reg, fix)
        print(s)
        return s

    # Get subjects of the input using SpaCy
    def subfinder(self, input):
        nlp = spacy.load('C:\\Users\\Mark\\Anaconda2\\envs\\newmark\\Lib\\site-packages\\en_core_web_sm\\en_core_web_sm-2.0.0')
        doc = nlp(input)

        narray = []
        index = -1
        counter = 0

        for np in doc.noun_chunks:
            for word in np:
                if word.dep_ == "nsubj":
                    index = counter
            narray.append(np)
            counter = counter + 1
        return narray[index]

    # Turns input into a form the database can accept
    def storeInput(self, input):
        sentences = []
        # Seperate input into sentences
        input = self.cleanUp(input)
        print(input)
        # Lemmatize input
        # Get subjects
        for line in input:
            print(line)
            # Put a space between the last letter and the period
            if line == '':
                break
            # Put a space before the period
            if line[len(line) - 1] == '.':
                line = line[:-1] # Remove period if there is one
            line = line + ' .'
            # Get the subject
            sub = self.subfinder(line)
            # sub = 'test'
            # Store input into Sentence objects by their subjects
            holdsent = Sentence(line, sub, sr.response(line))
            # Store Sentence object into an array
            sentences.append(holdsent)
        # return list of objects
        return sentences
