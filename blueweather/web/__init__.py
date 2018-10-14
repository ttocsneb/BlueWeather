import logging
import logging.config

import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


from blueweather import variables, plugin

from blueweather.web import config, server
from blueweather.web.util import template


logger = logging.getLogger(__name__)


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()


def init_db():
    from .users import models
    db.create_all()
    if models.User.query.count() == 0:
        logger.info(
            "No users exist, creating default user: 'root', pass='password'")

        password_hash = bcrypt.generate_password_hash('password')

        user = models.User(username='root',
                           password=password_hash)
        permissions = models.Permission(user_id=user.id,
                                        change_perm=True,
                                        add_user=True, reboot=True,
                                        change_settings=True)
        user.permissions = permissions

        db.session.add(user)
        db.session.add(permissions)
        db.session.commit()


def register_static_folder(name: str, import_name: str, folder: str):
    blueprint = flask.Blueprint(name, import_name,
                                static_url_path='/static/' + name,
                                static_folder=folder)
    flask.current_app.register_blueprint(blueprint)


def start(debug=False):
    app = Flask(__name__)
    app.config.from_object(config.Config())

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from .users.routes import users
        from .util.routes import data
        from .main.routes import main
        from .errors.handlers import errors
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(data)
        app.register_blueprint(errors)

        init_db()

        variables.plugin_manager.loadPlugins()
        variables.plugin_manager.activatePlugins()

    host = variables.config.web.host
    port = variables.config.web.port

    variables.plugin_manager.call(plugin.types.StartupPlugin,
                                  plugin.types.StartupPlugin.on_startup,
                                  args=(host, port))

    template.load_templates()

    # Register all the plugin routes
    routes = list()
    variables.plugin_manager.call(plugin.types.RoutePlugin,
                                  plugin.types.RoutePlugin.get_bluprint,
                                  return_list=routes)
    for route in routes:
        app.register_blueprint(route['returned'])

    if debug is True:
        app.run(host, port, debug=True)
    else:
        server.startServer(host, port, app)
