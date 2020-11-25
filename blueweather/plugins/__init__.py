from blueweather.config import Config

from . import manager

from .apps import config, conversion, weather


class Plugins:
    """
    Manager for all plugins

    :param conf: config
    """
    def __init__(self, conf: Config):
        self.conversions = manager.PluginManager(conversion.getConversions)
        self.configs = manager.PluginManager(config.getSettings)
        self.weather = manager.DriverManager(
            conf.plugins.weather_driver,
            weather.getWeather
        )

    def load(self):
        """
        Load the plugins
        """
        self.conversions.load()
        self.configs.load()
        self.weather.load()
