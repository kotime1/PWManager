from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize the Flask application
app = Flask(__name__)


# Load configurations from config.json
with open('PWManager/config.json') as config_file:
    config = json.load(config_file)
    app.config.update(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Flask-Bcrypt
db = SQLAlchemy(app)

from PWManager import models, routes

if __name__ == '__main__':
    app.run()