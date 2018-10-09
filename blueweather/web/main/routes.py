import flask
from flask import url_for
import flask_login
from flask_login import login_required

from blueweather import variables
from blueweather.web.util import template

from .util import get_web_variables


main = flask.Blueprint('main', __name__)


@main.route('/isDown')
def isDown():
    return 'Nope.'


@main.route('/')
def home():
    # In the future, I would like to dynamically generate this dict
    pages = {
        url_for('main.dashboard'): dashboard,
        url_for('main.data'): data
    }
    page = pages.get(variables.config.web.home_page, None)

    # If the page is not in the default set of pages, just redirect to the page
    if not page:
        return flask.redirect(variables.config.web.home_page)

    # Render the page if is a default page
    return page()


@main.route('/dashboard')
def dashboard():

    web = get_web_variables('main.dashboard', 'Dashboard')

    statusCard = variables.load_status()
    if len(statusCard['messages']) is 0 and len(statusCard['tables']) is 0:
        statusCard = None
    return flask.render_template('dashboard.jinja2',
                                 status=statusCard,
                                 **web)


@main.route('/weather')
def data():
    web = get_web_variables('main.data', 'Dashboard')

    weatherCard = variables.load_weather()
    if len(weatherCard['tables']) is 0:
        weatherCard = None
    return flask.render_template('weather.jinja2',
                                 weather=weatherCard,
                                 **web)


@main.route('/config')
@login_required
def config():

    if flask_login.current_user.permissions.change_settings is False:
        flask.abort(403)

    settings = template.render_templates(template.get_templates('settings'))

    web = get_web_variables('main.config', 'Dashboard')
    return flask.render_template('config.jinja2', settings=settings,
                                 **web)
