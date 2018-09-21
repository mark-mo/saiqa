from flask import render_template
from saiqa import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    print('Index')
    return render_template('index.html', title='Home', user=user)