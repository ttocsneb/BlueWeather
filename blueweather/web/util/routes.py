import flask
from flask import current_app

from blueweather import variables, plugin

from . import template

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


@data.route('/data/status')
def status():
    variables.plugin_manager.call(
        plugin.types.WeatherPlugin,
        plugin.types.WeatherPlugin.on_weather_request,
        call_time=5)
    statusCards = template.render_templates(template.get_templates('status'))
    return flask.render_template('includes/status.jinja2', status=statusCards)


@data.route('/data/weather')
def weather():
    variables.plugin_manager.call(
        plugin.types.WeatherPlugin,
        plugin.types.WeatherPlugin.on_weather_request,
        call_time=5)
    weatherCards = template.render_templates(template.get_templates('weather'))
    return flask.render_template('includes/weather.jinja2',
                                 weather=weatherCards)


@data.route('/status/remove_message')
def remove_message():
    if flask.request.args.get('id'):
        variables.status.setStatusMessage(key=flask.request.args.get('id'))
        return status()
    return 'false'
