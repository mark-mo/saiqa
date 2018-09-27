"""
This script runs the SAIQA application using a development server.
"""

from os import environ
from SAIQA import app

"""

"""
import sys, os.path
sys.path.append('D:/home/site/tools/Lib/site-packages')

if __name__ == '__main__':
    print('Python Ver:', sys.version)
    HOST = environ.get('SERVER_HOST', 'saiqa.azurewebsites.net')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
