import logging
import logging.config

import requests
import threading
import time

logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
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


logger = logging.getLogger(__name__)


def main(debug=False):
    logger.info("Starting BlueWeather")

    web.main(debug)
