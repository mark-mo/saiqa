from django.urls import path

from . import views
from .Controller import MainController
from .Controller import LoginController
from .Controller import QuestionController

urlpatterns = [
    path('', MainController.index, name='index'),
    path('main/', MainController.main, name='main'),
    path('about/', MainController.about, name='about'),
    path('login/', LoginController.login, name='login'),
    path('loginuser/', LoginController.loginuser, name='loginuser'),
    path('reg/', LoginController.login, name='login'),
    path('reguser/', LoginController.loginuser, name='loginuser'),
    path('question/', QuestionController.question, name='question'),
    path('answer/', QuestionController.answer, name='answer'),
    path('understand/', QuestionController.understand, name='understand'),
]