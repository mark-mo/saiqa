#A simple controller for logging in and registering
# Created by Mark Mott
from flask import Blueprint, render_template, request, redirect, session, url_for

from Sima.Model.UserModel import User
from Sima.Service.UserService import UserService
from Sima.Utility.LoggingDecorator import Loggingdec

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators
import json

login_controller = Blueprint('login_controller', __name__, template_folder='templates')
logging = Loggingdec()

service = UserService()

@login_controller.route('/login', methods=['GET', 'POST'])
def login():
    logging.entry("LoginController.login")
    form = LoginForm(request.form)
    if form.validate():  # Stop user from getting here before going to login page
        user = User(form.username.data, form.password.data)
        print('Registering...')
        # Log in
        if not (service.findUser(user)):
            return "User not found"
        session['user'] = json.dumps(user.toString())
        print('Thanks for Logging in')
        return redirect('/question')
    return render_template('login.html', title='Login', form=form)

@login_controller.route('/reg', methods=['GET', 'POST'])
def reg():
    logging.entry("LoginController.reg")
    form = RegistrationForm(request.form)
    if form.validate():  # Stop user from getting here before going to login page
        user = User(form.username.data, form.password.data)
        print(user._username) # DELETE once fixed
        # Log in
        if not (service.createUser(user)):
            logging.exit("LoginController.reg")
            return "User not found"
        logging.exit("LoginController.reg")
        return redirect('login')
    logging.exit("LoginController.reg")
    return render_template('register.html', title='Register', form=form)


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4,max=25)])
    password = PasswordField('Password', [validators.Length(min=4,max=25)])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign In')