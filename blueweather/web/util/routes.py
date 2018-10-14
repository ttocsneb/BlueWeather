import flask
from flask import current_app

from blueweather import variables, plugin

data = flask.Blueprint('data', __name__)


@current_app.before_first_request
def before_first_request():
    variables.plugin_manager.call(plugin.types.StartupPlugin,
                                  plugin.types.StartupPlugin.on_after_startup)


@current_app.before_request
def before_request():
    variables.plugin_manager.call(plugin.types.RequestsPlugin,
                                  plugin.types.RequestsPlugin.before_request,
                                  args=(flask.request.path, flask.request.args)
                                  )
