# django-saiqa
# A simple controller for handling questions and learning. Not implemented yet
# Created by Mark Mott
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import numpy as np
import json

from saiqa.Model.UserModel import User
from saiqa.Model.Sentence import Sentence
from saiqa.Service.QuestionService import *
from saiqa.Utility.LoggingDecorator import *
from saiqa.Utility.InputHandler import *
from saiqa.Utility.GloveHandler import *
import saiqa.Training.DMNInner as dmn
import saiqa.Training.importData as id
# Handles logging.
logging = Loggingdec()

# Initialize classes
question_service = QuestionService()
inputhandler = InputHandler()
# Does not work with Pytest
glovehandler = GloveHandler()

# Handles entering the question panel
# TODO: Add a decorator to only let admins have access to this method
def question(request):
    logging.entry("QuestionController.question")
    user = request.session['user']
    history_store = []
    if 'history' not in request.session:
        history = 'Hello '+ user['username'] + ', welcome to SAI-QA.  What question do you have today?'
        history_store.append(history)
        request.session['history'] = history
    print(request.session['history'])
    context = {
        'user': request.session['user'],
        'history': request.session['history'],
    }
    logging.exit("QuestionController.question")
    if user['permission'] == 2:
        return render(request, 'saiqa/questionAPanel.html', context)
    return render(request, 'saiqa/questionPanel.html', context)

# Answer the question
# TODO: Change to Ajax
def answer(request):
    logging.entry("QuestionController.answer")
    res = request.body
    deres = res.decode('utf-8')
    # Get user from the session
    data = request.session['user']
    history = request.session['history']
    history_load = history
    if isinstance(history, str):
        print('String')
        history_load = []
        history_load.append(history)
    
    # Return a random fact from the subject most often searched for by the user
    if deres == 'random':
        freqout = question_service.findbyfrequent(data["username"])
        # Save response to session
        history_load.append(deres)
        history_load.append(freqout)
        request.session['history'] = history_load
        logging.exit("QuestionController.answer")
        return JsonResponse(history_load, safe=False)
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
            history_load.append(deres)
            history_load.append('Could not find anything on ' + str(currsub) + '.')
            request.session['history'] = history_load
            
            logging.exit("QuestionController.answer")
            return JsonResponse(history_load, safe=False)
        
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
        # TODO: Update Answer and History sides
        history_load.append(deres)
        history_load.append(answer)
        request.session['history'] = history_load
        logging.exit("QuestionController.answer")
        return JsonResponse(history_load, safe=False)

# Handles entering the learning panel and training off of input, requires port 9000 open
# TODO: Add a decorator to only let admins have access to this method
def understand(request):
    user = request.session['0']
    # Get list of unknown nouns
    nounpath = os.getcwd() + "/saidj/weights/unknown.csv"
    nounlist = np.loadtxt(nounpath, delimiter=",")
    
    context = {
        'user': request.session['0'],
    }
    return render(request, 'saiqa/learnmod.html', context)

def learn(request):
    logging.entry("QuestionController.train")
    # Commented out for testing
    user = request.session['user']
    # Get information from the form
    sentences = request.POST.get('sent')
    ref = request.POST.get('source')
    rely = request.POST.get('trust')
    # Implement InputHandler
    output = inputhandler.storeInput(sentences)
    
    # Send Sentence models to database
    response = question_service.createSents(output, ref, rely)
    #print(response)
    # TODO: Get list of unknown nouns from file
    logging.exit("QuestionController.train")
    
    context = {
        'user': request.session['0'],
    }
    return render(request, 'saiqa/learnmod.html', context)

def answerrest(request):
    logging.entry("QuestionController.answer")
    res = request.body
    deres = res.decode('utf-8')
    # Get user from the session
    history_load = history
    if isinstance(history, str):
        print('String')
        history_load = []
        history_load.append(history)
    
    # Return a random fact from the subject most often searched for by the user
    if deres == 'random':
        freqout = question_service.findbyfrequent(data["username"])
        return JsonResponse(frequout, safe=False)
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
            logging.exit("QuestionController.answer")
            return JsonResponse('Could not find anything on ' + str(currsub) + '.', safe=False)
        
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
        return JsonResponse(answer, safe=False)