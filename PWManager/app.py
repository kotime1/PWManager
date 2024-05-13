from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize the Flask application
app = Flask(__name__, template_folder='templates')

# Load configurations from config.json
with open('PWManager/config.json') as config_file:
    config = json.load(config_file)
    app.config.update(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Flask SQLAlchemy
db = SQLAlchemy(app)

from models import User

def setup_db():
    with app.app_context():
        db.create_all()

import routes