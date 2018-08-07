import flask
from flask import url_for
from flask_login import login_required

from . import users
from . import data

import blueweather.data

main = flask.Blueprint('main', __name__)


@main.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    blueweather.data.setStatusMessage('message', 'Hello World!')
    status = blueweather.data.getStatus()
    if len(status['messages']) is 0 and len(status['data']) is 0:
        status = None
    return flask.render_template('dashboard.html', breadcrumbs=breadcrumb,
                                 status=status)


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
