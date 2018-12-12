from flask import Flask
from Sima.Controller.MainController import main_controller
from Sima.Controller.LoginController import login_controller
from Sima.Controller.QuestionController import question_controller
"""

"""
import sys, os.path
sys.path.append('D:/home/site/tools/Lib/site-packages')
print('Python Ver:', sys.version)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'
app.register_blueprint(main_controller)
app.register_blueprint(login_controller)
app.register_blueprint(question_controller)

import Sima.Controller.MainController
import Sima.Controller.LoginController
import Sima.Controller.QuestionController