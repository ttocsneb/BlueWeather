import flask

from blueweather import variables

data = flask.Blueprint('data', __name__)


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
