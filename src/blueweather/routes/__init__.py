import flask
from flask import url_for
from flask_login import login_required

from . import users

main = flask.Blueprint('main', __name__)


@main.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    return flask.render_template('dashboard.html', breadcrumbs=breadcrumb)


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
