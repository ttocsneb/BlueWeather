import flask
from flask import url_for
import flask_login
from flask_login import login_required

from blueweather import variables
from blueweather.web.util import template
from blueweather.plugin import types

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

    variables.plugin_manager.call(types.WeatherPlugin,
                                  types.WeatherPlugin.on_weather_request,
                                  call_time=5)
    status = template.render_templates(template.get_templates('status'))

    statusCards = template.render_templates(
        template.get_templates('dashboard_page'))

    return flask.render_template('dashboard.jinja2',
                                 status=status, dashboard_page=statusCards,
                                 **web)


@main.route('/weather')
def data():
    web = get_web_variables('main.data', 'Dashboard')

    variables.plugin_manager.call(types.WeatherPlugin,
                                  types.WeatherPlugin.on_weather_request,
                                  call_time=5)
    weather = template.render_templates(template.get_templates('weather'))

    weatherCards = template.render_templates(
        template.get_templates('weather_page'))

    return flask.render_template('weather.jinja2',
                                 weather=weather, weather_page=weatherCards,
                                 **web)


@main.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    from flask_wtf import FlaskForm
    import wtforms

    class SaveForm(FlaskForm):
        submit = wtforms.SubmitField('Save')

    form = SaveForm()

    if form.validate_on_submit():
        variables.config.save()
        flask.flash('Successfully Saved settings', category='success')
        return flask.redirect(url_for('main.home'))

    if flask_login.current_user.permissions.change_settings is False:
        flask.abort(403)

    settings = template.render_templates(template.get_templates('settings'))

    web = get_web_variables('main.config', 'Dashboard')
    return flask.render_template('config.jinja2', settings=settings,
                                 form=form, **web)
