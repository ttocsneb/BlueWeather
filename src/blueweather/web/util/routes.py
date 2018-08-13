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
                                  args=(flask.request.path, flask.request.args))


@data.route('/data/status')
def status():
    statusData = variables.load_status()
    return flask.render_template('includes/status.html', status=statusData)


@data.route('/data/weather')
def weather():
    weatherData = variables.load_weather()
    return flask.render_template('includes/weather.html', weather=weatherData)


@data.route('/status/remove_message')
def remove_message():
    if flask.request.args.get('id'):
        variables.status.setStatusMessage(key=flask.request.args.get('id'))
        return status()
    return 'false'
