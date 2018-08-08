import blueweather
from blueweather.plugin import types


class TestPlugin(types.StartupPlugin):

    def on_startup(self, host, port):
        self._logger.info("Hello World! AAAAAAAAAAAAAAAAA")
