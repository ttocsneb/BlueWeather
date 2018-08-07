import flask

import blueweather.data

data = flask.Blueprint('data', __name__)


@data.route('/data/status', methods=['POST'])
def status():
    return blueweather.data.getJSONStatus()
