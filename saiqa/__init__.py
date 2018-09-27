"""
The flask application package.
"""

from flask import Flask

import sys, os.path
sys.path.append('D:/home/site/tools/Lib/site-packages')
print('Python Ver:', sys.version)

app = Flask(__name__)

import SAIQA.views
