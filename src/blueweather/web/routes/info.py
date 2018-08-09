import flask

from blueweather import variables

data = flask.Blueprint('data', __name__)


@data.route('/data/status', methods=['POST'])
def status():
    return variables.status.getJSONStatus()
