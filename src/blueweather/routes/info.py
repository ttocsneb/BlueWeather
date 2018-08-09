import flask

from blueweather import weather

data = flask.Blueprint('data', __name__)


@data.route('/data/status', methods=['POST'])
def status():
    return weather.status.getJSONStatus()
