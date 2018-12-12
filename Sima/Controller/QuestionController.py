#A simple controller for logging in and registering
# Created by Mark Mott
from flask import Blueprint, render_template, request, session

from Sima.Model.UserModel import User
from Sima.Utility.LoggingDecorator import Loggingdec

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import json

question_controller = Blueprint('question_controller', __name__, template_folder='templates')
logging = Loggingdec()

# Handles entering the question panel
@question_controller.route('/question', methods=['GET', 'POST'])
def question():
    logging.entry("QuestionController.question")
    user = session['user']
    data = json.loads(user)
    form = QuestionForm(request.form)
    # TODO: If the user is an admin, go to a different page
    if request.method == 'POST' and form.validate():
        if request.form['submit_button'] == 'Question': 
            # TODO: Answer question
            # TODO: Update Answer and History sides
            logging.exit("QuestionController.question")
            return "Not yet implemented"
        if request.form['submit_button'] == 'Logout':
            # TODO: Remove user from session
            logging.exit("QuestionController.question")
            return redirect(url_for('home')) # Goes to the Register logic
    logging.exit("QuestionController.question")
    return render_template('questionPanel.html', title='Question', user=data['username'], form=form)

# Handles entering the traing panel and training off of input
@question_controller.route('/train')
def train():
    logging.entry("QuestionController.train")
    user = session['user']
    data = json.loads(user)
    logging.exit("QuestionController.train")
    return render_template('train.html', title='Train', user=data['username'])

# Called by AJAX to update the responses
@question_controller.route('/_answer')
def updateAnswer():
    logging.entry("QuestionController.updateAnswer")
    list = [] # TODO Get list of current conversation with Sima
    logging.exit("QuestionController.updateAnswer")
    return jsonify(result=list)

# Called by AJAX to update the history
@question_controller.route('/_history')
def updateHistory():
    logging.entry("QuestionController.updateHistory")
    list = [] # TODO Get list of current conversation with who wrote what annotated
    logging.exit("QuestionController.updateHistory")
    return jsonify(result=list)

# Handles creating the form to ask questions
class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Enter Question Here...')