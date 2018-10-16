import flask

from blueweather.web.main.util import get_web_variables

errors = flask.Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return flask.render_template(
        'errors/404.jinja2',
        **get_web_variables(title='404')), 404


@errors.app_errorhandler(403)
def error_403(error):
    return flask.render_template(
        'errors/403.jinja2',
        **get_web_variables(title='403')), 403


@errors.app_errorhandler(500)
def error_500(error):
    return flask.render_template(
        'errors/500.jinja2',
        **get_web_variables(title='500')), 500
