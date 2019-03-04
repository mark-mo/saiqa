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
import saiqa.Training.DMNInner as dmn
import saiqa.Training.importData as id
# Handles logging.
# TODO: Change to decorator
logging = Loggingdec()

# Initialize classes
question_service = QuestionService()
inputhandler = InputHandler()

# Handles entering the question panel
# TODO: Add a decorator to only let admins have access to this method
def question(request):
    logging.entry("QuestionController.question")
    user = request.session['user']
    history_store = []
    if 'history' not in request.session:
        history = 'Hello '+ user['username'] + ', welcome to SAI-QA.  What question do you have today?'
        history_store.append(history)
        request.session['history'] = history_store
    print(request.session['history'])
    context = {
        'user': request.session['user'],
        'history': request.session['history'],
    }
    logging.exit("QuestionController.question")
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
    #history_load = json.loads(history)
    print(history)
    # TODO: If the user is an admin, go to a different page
    # Get subject and category
    cat_sent = inputhandler.storeInput(deres)[0]
    
    response = question_service.findbysubject(cat_sent.getsubject(), cat_sent.getcategory())
    
    sentences = []
    cleanedSents = []
    for line in response:
        #sentence, subject, category
        sentences.append(Sentence(line[2], line[1], line[3]))
        cleanedSents.append(line[2])
    answer = dmn.dmnrun(cleanedSents, cat_sent.getsentence())
    # TODO: Update Answer and History sides
    history.append(deres)
    history.append(answer)
    # request.session['history'] = json.dumps(history_load)
    request.session['history'] = json.dumps(history)
    logging.exit("QuestionController.answer")
    return JsonResponse(history, safe=False)

# Handles entering the learning panel and training off of input, requires port 9000 open
# TODO: Add a decorator to only let admins have access to this method
def understand(request):
    user = request.session['0']
    print(user)
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
    print(sentences)
    output = inputhandler.storeInput(sentences)
    
    # For testing
    for line in output:
        print(line.getsubject())
    
    # Send Sentence models to database
    response = question_service.createSents(output, ref, rely)
    #print(response)
    # TODO: Get list of unknown nouns from file
    logging.exit("QuestionController.train")
    
    context = {
        'user': request.session['0'],
    }
    return render(request, 'saiqa/learnmod.html', context)
    