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


# This is a bit of a weird hack
# It polls the server until it responds with a 200 code. when this happens,
# the before_first_request gets called which calls the on_after_startup
# function in the plugins
def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            logger.debug("Checking if server is started")
            try:
                r = requests.get('http://127.0.0.1:5000')
                if r.status_code is 200:
                    logger.debug('Server started')
                    not_started = False
                    return
                logger.debug(r.status_code)
            except:
                pass
            logger.debug("Server not yet started")
            time.sleep(1)

    thread = threading.Thread(target=start_loop)
    thread.start()


def main(debug=False):
    logger.info("Starting BlueWeather")

    start_runner()

    web.main(debug)
