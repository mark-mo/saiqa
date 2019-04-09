from saiqa.Model.UserModel import User
from saiqa.Model.Sentence import Sentence
from saiqa.Service.QuestionService import *
from saiqa.Utility.LoggingDecorator import *
from saiqa.Utility.InputHandler import *
from saiqa.Utility.GloveHandler import *

# Initialize classes
question_service = QuestionService('local')
inputhandler = InputHandler()
glovehandler = GloveHandler()

# List of tests:
#   Correct Upload of Information
#   Clean upload of information
#   Enter a non-digit for trust level
#   Leave any field blank
def testunderstand(sentences, ref, rely, user):
    if sentences == '' | ref == '' | rely == '':
        return 'Bad upload'
    elif type(rely) != type(2):
        return 'Not a number'
    # Implement InputHandler
    output = inputhandler.storeInput(sentences)
    
    # Send Sentence models to database
    response = question_service.createSents(output, ref, rely)
    return response

# List of tests:
#   Ask a valid question
#   Ask a question about a semi-known subject
#   Ask a question about an unknown subject
#   Ask for a random fact from a frequently asked for subject
# Return a random fact from the subject most often searched for by the user
def testanswer(deres, username):
    if defes == '':
        return 'Bad question'
    # Return a random entry based on the user
    if deres == 'random':
        freqout = question_service.findbyfrequent(username)
        return freqout
    else:
        # Get subject and category
        cat_sent = inputhandler.storeInput(deres)[0]
        
        currsub = cat_sent.getsubject()
        response = question_service.findbysubject(cat_sent.getsubject(), cat_sent.getcategory(), data["username"])
        
        attempt = 1
        # Try and change the subject if no information is found
        if response[0] == 'Nothing':
            while attempt < 4:
                newsubject = glovehandler.findnearest(currsub)
                # If the subject is not in the vocabulary, do not try again
                if newsubject[0] == '-':
                    break
                print('Trying ' + newsubject)
                response = question_service.findbysubject(currsub, cat_sent.getcategory(), data["username"])
                if response[0] != 'Nothing':
                    break
                print(newsubject + 'not found')
                attempt = attempt + 1
        
        # If nothing is found surrounding the subject, return a negative
        if response[0] == 'Nothing':
            return 'Could not find anything on ' + currsub
        
        sentences = []
        cleanedSents = []
        # Create Sentence objects
        for line in response:
            # Ensure each sentence has a period at the end
            send = line[2] # Created to solve an error
            if send.count('.') == 0:
                send = send + '.'
            sentences.append(Sentence(send, line[1], line[3]))
            cleanedSents.append(send)
        answer = dmn.dmnrun(cleanedSents, cat_sent.getsentence())
        return answer