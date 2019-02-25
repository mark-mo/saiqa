#A simple controller for logging in and registering
# Created by Mark Mott
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from saiqa.Model.UserModel import User
from saiqa.Service.UserService import UserService
from saiqa.Utility.LoggingDecorator import Loggingdec
import json

# Handles logging.
# TODO: Change to decorator
logging = Loggingdec()

service = UserService()

# Goes to login
def login(request):
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/login.html', context)

def loginuser(request):
    logging.entry("LoginController.loginuser")
    
    if request.method == 'POST':
        user = User(request.POST.get('username'), request.POST.get('password'))
        # Log in
        if not (service.findUser(user)):
            logging.exit("LoginController.login")
            return redirect('/saiqa/login/')
        request.session['user'] = user.__dict__ # Puts the user into the session
        history = ['Hello '+ user.getusername() + ', welcome to SAI-QA.  What question do you have today?']
        request.session['history'] = json.dumps(history)
        print('Thanks for Logging in')
        logging.exit("LoginController.login")
        if user.getpermission() == 2:
            redirect('/saiqa/understand/')
        return redirect('/saiqa/question/')

# Goes to registration
def reg(request):
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/register.html', context)

def reguser(request):
    logging.entry("LoginController.reguser")
    
    user = User(request.POST.get('username'), request.POST.get('password'))
    request.session[0] = user
    # If true, the user exists
    if not (service.createUser(user)):
        logging.exit("LoginController.reguser")
        return redirect("/reg")
    # TODO: Pass in a random fact from the database
    logging.exit("LoginController.reguser")
    return redirect("/question")

# Test login
def _testlogin(user):
    return service.createUser(user) # Check if user exists