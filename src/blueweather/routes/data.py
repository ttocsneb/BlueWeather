import flask

from blueweather import status as blueStatus

data = flask.Blueprint('data', __name__)


@data.route('/data/status', methods=['POST'])
def status():
    return blueStatus.getJSONStatus()
