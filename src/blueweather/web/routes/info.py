import flask

from blueweather import variables

data = flask.Blueprint('data', __name__)


@data.route('/data/status')
def status():
    statusData = variables.load_status()
    return flask.render_template('includes/status.html', status=statusData)


@data.route('/status/remove_message')
def remove_message():
    if flask.request.args.get('id'):
        variables.status.setStatusMessage(key=flask.request.args.get('id'))
        return status()
    return 'false'
