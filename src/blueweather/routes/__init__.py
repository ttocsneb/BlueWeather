import flask
from flask import url_for
from flask_login import login_required

from blueweather import status

from . import users
from . import data


main = flask.Blueprint('main', __name__)


@main.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    status.setStatusMessage('message', 'Hello World!')
    statusCard = status.getStatus()
    if len(statusCard['messages']) is 0 and len(statusCard['data']) is 0:
        statusCard = None
    return flask.render_template('dashboard.html', breadcrumbs=breadcrumb,
                                 status=statusCard)


@main.route('/weather')
def weather():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('main.home')
        },
        {
            'name': 'weather'
        }
    ]
    return flask.render_template('layouts/web.html', title='Weather',
                                 breadcrumbs=breadcrumb)


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
