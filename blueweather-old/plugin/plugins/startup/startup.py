"""
This is a bit of a weird hack
It polls the server on startup until it responds with a 200 code. when
this happens,the before_first_request gets called which calls the
on_after_startup function in the plugins.
"""

import threading
import time
import requests

from blueweather.plugin.types import StartupPlugin


class Startup(StartupPlugin):

    def __init__(self):
        super(Startup, self).__init__()
        self._port = 5000

    def start_loop(self):
        not_started = True
        while not_started:
            self._logger.debug("Checking if server is started")
            try:
                r = requests.get(
                    'http://127.0.0.1:{0}/isDown'.format(self._port))
                if r.status_code == 200:
                    self._logger.debug('Server started')
                    not_started = False
                    return
                self._logger.debug(r.status_code)
            except:
                pass
            self._logger.debug("Server not yet started")
            time.sleep(1)

    def on_startup(self, host, port):
        self._port = port
        thread = threading.Thread(target=self.start_loop)
        thread.start()

    def on_after_startup(self):
        self._logger.info("Server is online")
