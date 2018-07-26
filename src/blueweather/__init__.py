from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# TODO: generate a secret key if the secret key doesn't already exist
app.config['SECRET_KEY'] = 'ec5b916be3348b6c695ced12ade929e9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# prevent circular imports
from blueweather import routes


def main(debug=False):
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug)
