"""
This script runs the SAIQA application using a development server.
"""

from os import environ
from saiqa import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'saiqa.azurewebsites.net')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
