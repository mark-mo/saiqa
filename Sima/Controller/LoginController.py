#A simple controller for logging in and registering
# Created by Mark Mott
from flask import Blueprint, render_template, request, redirect, session, url_for

from Sima.Model.UserModel import User
from Sima.Service.UserService import UserService
from Sima.Utility.LoggingDecorator import Loggingdec

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators
import json

# Creates a way for routes outside of this script to work
login_controller = Blueprint('login_controller', __name__, template_folder='templates')
# Handles logging.
# TODO: Change to decorator
logging = Loggingdec()

service = UserService()

# Handles logging in using a FlaskForm
@login_controller.route('/login', methods=['GET', 'POST'])
def login():
    logging.entry("LoginController.login")
    form = LoginForm(request.form)
    if form.validate():  # Stop user from getting here before going to login page
        user = User(form.username.data, form.password.data)
        print('Registering...')
        # Log in
        if not (service.findUser(user)):
            logging.exit("LoginController.login")
            return "User not found" # Change to an actual error
        session['user'] = json.dumps(user.toString()) # Puts the user into the database, might change to use Flask-login
        print('Thanks for Logging in')
        logging.exit("LoginController.login")
        return redirect('/question')
    # TODO: Pass in a random fact from the database
    logging.exit("LoginController.login")
    return render_template('login.html', title='Login', form=form) # Have page display errors

# Handles registering using a FlaskForm
@login_controller.route('/reg', methods=['GET', 'POST'])
def reg():
    logging.entry("LoginController.reg")
    form = RegistrationForm(request.form)
    if form.validate():  # Stop user from getting here before going to login page
        user = User(form.username.data, form.password.data)
        # If true, the user exists
        if not (service.createUser(user)):
            logging.exit("LoginController.reg")
            return "User already exists" # Change to an actual error
        logging.exit("LoginController.reg")
        return redirect('login') # Go to login page once user is created to properly login
    # TODO: Pass in a random fact from the database
    logging.exit("LoginController.reg")
    return render_template('register.html', title='Register', form=form)

# Handles the logic and validation for login using a FlaskForm
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4,max=25)])
    password = PasswordField('Password', [validators.Length(min=4,max=25)])
    submit = SubmitField('Sign In')

# Handles the logic and validation for register using a FlaskForm
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match') # Ensures that password field matches confirm
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign In')