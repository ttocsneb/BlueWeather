import blueweather
from blueweather.plugin import types


class TestPlugin(types.StartupPlugin):

    def on_startup(self, host, port):
        self._logger.info("Hello World!")
    
    def on_after_startup(self):
        self._logger.info("After Startup! Cool")
