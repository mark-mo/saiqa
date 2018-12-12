#A simple controller for the main page of the application
# Created by Mark Mott
from flask import Blueprint, render_template, request, redirect, session

from Sima.Utility.LoggingDecorator import Loggingdec

main_controller = Blueprint('main_controller', __name__, template_folder='templates')
logging = Loggingdec()

# Handles going to the main page and going to the login or register page
@main_controller.route('/')
@main_controller.route('/index')
def showMain():
    logging.entry("MainController.showMain")
    if request.args.get('submit_button') == 'Login': # Executes after a button is pressed in index.html
        # TODO: Add a random fact from the database
        logging.exit("MainController.showMain")
        return redirect('login') # Goes to the Login logic
    if request.args.get('submit_button') == 'Register':
        # TODO: Add a random fact from the database
        print('reg')
        logging.exit("MainController.showMain")
        return redirect('reg') # Goes to the Register logic
    elif request.method == 'GET':
        logging.exit("MainController.showMain")
        return render_template('index.html', title='Home')

# Method to enter the about page for the application
@main_controller.route('/about')
def showAbout():
    logging.entry("MainController.showAbout")
    # TODO: Add a random fact from the database
    logging.exit("MainController.showAbout")
    return render_template('about.html', title='About')

# Method to logout of the application
@main_controller.route('/logout')
def logoutUser():
    session.clear()
    return redirect('/') # Goes to the main page
    