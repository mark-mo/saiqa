from flask import render_template
from saiqa import app
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# matplotlib inline
import scipy.sparse

import saiqa.softmaxR as sm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    print('Index')
    return render_template('index.html', title='Home', user=user)

@app.route('/soft')
def softmaxR():
    input = 'The Moon orbits the earth.'
    resp = sm.response(input)
    out = {'soft':resp}
    return render_template('soft.html', title='Softmax', out=out)