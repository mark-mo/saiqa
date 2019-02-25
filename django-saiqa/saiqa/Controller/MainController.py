# For the saiqa app
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader

from saiqa.Model.UserModel import User

# Default route, only purpose is to set a guest user
def index(request):
    user = User()
    request.session['user'] = user.__dict__ # Puts the user into the session
    print(request.session['user'])
    return redirect('/saiqa/main/')

# Create your views here.
def main(request):
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/index.html', context)

# Go to the about page
def about(request):
    context = {
        'user_list': 'hold',
    }
    return render(request, 'saiqa/about.html', context)