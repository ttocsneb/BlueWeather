import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s - %(name)s: %(message)s'
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from blueweather import web
from blueweather import variables
from blueweather.plugin import types


logger = logging.getLogger(__name__)


def main(debug=False):
    from . import gitsubmodule
    gitsubmodule.load_git_submodules()

    logger.info("Starting BlueWeather")

    web.start(debug)

    variables.plugin_manager.call(types.StartupPlugin,
                                  types.StartupPlugin.on_shutdown)
