from blueweather.config import Config

from . import manager

from .apps import config, conversion, weather


# default_app_config = "blueweather.plugins.apps.ExtensionsConfig"


class Plugins:
    """
    Manager for all plugins

    :param conf: config
    """
    def __init__(self, conf: Config):
        self.conversions = manager.PluginManager("Conversion", conversion.getConversions)
        self.configs = manager.PluginManager("Config", config.getSettings)
        self.weather = manager.DriverManager(
            conf.plugins.weather_driver,
            "Weather",
            weather.getWeather
        )

    def load(self):
        """
        Load the plugins
        """
        self.conversions.load()
        self.configs.load()
        self.weather.load()
