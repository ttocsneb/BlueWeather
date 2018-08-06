import flask
from flask import url_for
import flask_login
from flask_login import login_required

from blueweather import forms, models
from blueweather import app, db, bcrypt

routes = flask.Blueprint('routes', __name__)
from . import users


@routes.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    return flask.render_template('dashboard.html', breadcrumbs=breadcrumb)


@routes.route('/weather')
def weather():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('routes.home')
        },
        {
            'name': 'weather'
        }
    ]
    return flask.render_template('layouts/web.html', title='Weather',
                                 breadcrumbs=breadcrumb)


@routes.route('/config')
@login_required
def config():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('routes.home')
        },
        {
            'name': 'config'
        }
    ]
    return flask.render_template('layouts/web.html', title='Config',
                                 breadcrumbs=breadcrumb)
