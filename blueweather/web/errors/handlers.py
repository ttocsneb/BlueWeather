import flask

errors = flask.Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return flask.render_template('errors/404.jinja2'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return flask.render_template('errors/403.jinja2'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return flask.render_template('errors/500.jinja2'), 500
