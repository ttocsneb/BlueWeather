import flask
from flask import url_for
from flask_login import login_required

from blueweather import variables


main = flask.Blueprint('main', __name__)


@main.route('/isDown')
def isDown():
    return 'Nope.'


@main.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]

    statusCard = variables.load_status()
    if len(statusCard['messages']) is 0 and len(statusCard['data']) is 0:
        statusCard = None
    return flask.render_template('dashboard.html', breadcrumbs=breadcrumb,
                                 status=statusCard)


@main.route('/weather')
def data():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('main.home')
        },
        {
            'name': 'weather'
        }
    ]

    weatherCard = variables.load_weather()
    return flask.render_template('weather.html', title='Weather',
                                 breadcrumbs=breadcrumb, weather=weatherCard)


@main.route('/config')
@login_required
def config():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('main.home')
        },
        {
            'name': 'config'
        }
    ]
    return flask.render_template('layouts/web.html', title='Config',
                                 breadcrumbs=breadcrumb)
