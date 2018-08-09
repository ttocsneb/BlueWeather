import logging
import logging.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


from blueweather import plugin, variables


logger = logging.getLogger(__name__)

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
from . import routes
from . import models


app.register_blueprint(routes.main)
app.register_blueprint(routes.users.users)
app.register_blueprint(routes.info.data)


def init_db():
    db.create_all()
    if models.User.query.count() == 0:
        logger.info(
            "No users exist, creating default user: 'root', pass='password'")

        user = models.User(username='root',
                           password=bcrypt.generate_password_hash('password'))
        permissions = models.Permission(user_id=user.id, change_perm=True,
                                        add_user=True, reboot=True,
                                        change_settings=True)
        user.permissions = permissions

        db.session.add(user)
        db.session.add(permissions)
        db.session.commit()


def main(debug=False):

    init_db()
    variables.plugin_manager.loadPlugins()
    variables.plugin_manager.activatePlugins()

    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000

    variables.plugin_manager.call(plugin.types.StartupPlugin,
                                  plugin.types.StartupPlugin.on_startup,
                                  HOST, PORT)

    app.run(HOST, PORT, debug)
