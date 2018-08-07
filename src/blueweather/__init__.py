from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# TODO: generate a secret key if the secret key doesn't already exist
app.config['SECRET_KEY'] = 'ec5b916be3348b6c695ced12ade929e9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

csrf = CSRFProtect(app)

# prevent circular imports
from blueweather import routes
from blueweather import models


db.create_all()
if models.User.query.count() == 0:
    user = models.User(username='root',
                       password=bcrypt.generate_password_hash('password'))
    permissions = models.Permission(user_id=user.id, change_perm=True,
                                    add_user=True, reboot=True,
                                    change_settings=True)
    user.permissions = permissions

    db.session.add(user)
    db.session.add(permissions)
    db.session.commit()

app.register_blueprint(routes.main)
app.register_blueprint(routes.users.users)
app.register_blueprint(routes.data.data)


def main(debug=False):
    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug)
