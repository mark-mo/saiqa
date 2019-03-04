#A simple controller for logging in and registering
# Created by Mark Mott
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from saiqa.Model.UserModel import User
from saiqa.Service.UserService import UserService
from saiqa.Service.QuestionService import QuestionService
from saiqa.Utility.LoggingDecorator import Loggingdec
from saiqa.Exception.CustomException import FormatError, PasswordMismatchError, EmptyFormError
import json
import re

# Handles logging.
# TODO: Change to decorator
logging = Loggingdec()

service = UserService()
qser = QuestionService()

# Goes to login
def login(request):
    # Get a random fact from the database
    randfact = qser.findByRandom()
    print(randfact)
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/login.html', context)

def loginuser(request):
    logging.entry("LoginController.loginuser")
    
    if request.method == 'POST':
        user = User(request.POST.get('username'), request.POST.get('password'))
        # Log in
        foundU = service.findUser(user)
        if foundU == -1:
            # Replace with error
            print('User not found')
            logging.exit("LoginController.login")
            return redirect('/saiqa/login/')
        user.setpermission(foundU)
        request.session['user'] = user.__dict__ # Puts the user into the session
        print(user.__dict__)
        history = ['Hello '+ user.getusername() + ', welcome to SAI-QA.  What question do you have today?']
        request.session['history'] = json.dumps(history)
        print('Thanks for Logging in')
        logging.exit("LoginController.login")
        if user.getpermission() == 2:
            print('Hello admin')
            return redirect('/saiqa/understand/')
        return redirect('/saiqa/question/')

# Goes to registration
def reg(request):
    # Get a random fact from the database
    randfact = qser.findByRandom()
    print(randfact)
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/register.html', context)

def reguser(request):
    logging.entry("LoginController.reguser")
    user = User(request.POST.get('username'), request.POST.get('password'))
    
    try:
        if user.getpassword() == '':
            raise EmptyFormError
        if user.getpassword() != request.POST.get('repassword'):
            raise PasswordMismatchError
    except PasswordMismatchError: # Kick the user back to the register screen
        logging.exit('Passwords do not match')
        context = {
            'user_list': 'hold',
        }
        return redirect('/saiqa/reg/')
    except EmptyFormError: # Kick the user back to the register screen
        logging.exit('Fill in the form')
        context = {
            'user_list': 'hold',
        }
        return redirect('/saiqa/reg/')
    
    specres = re.findall('[$&+,=?@`~^*%!-_]', user.getpassword())
    upres = re.findall('[A-Z]', user.getpassword())
    print(len(specres))
    print(len(upres))
    
    try:
        if(len(user.getusername()) < 4 or len(user.getusername()) > 20):
            raise FormatError
        if(len(user.getpassword()) < 4 or len(user.getpassword()) > 20):
            raise FormatError
        if(len(specres) < 2 or len(specres) < 2):
            raise FormatError
    except FormatError:
        logging.exit('Incorrect formating')
        context = {
            'user_list': 'hold',
        }
        return redirect('/saiqa/reg/')
        
    request.session['user'] = user.__dict__ # Puts the user into the session
    # If true, the user exists
    if not (service.createUser(user)):
        logging.exit("LoginController.reguser")
        print('User already created') # Switch to a logger
        return redirect("/saiqa/reg/")
    # TODO: Pass in a random fact from the database
    logging.exit("LoginController.reguser")
    return redirect("/saiqa/login/")

# Test login
def _testlogin(user):
    return service.createUser(user) # Check if user exists