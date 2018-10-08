import os
from pathlib import Path

# Prevent circular imports from plugin_manager
data_dir = os.path.join(str(Path.home()), '.blueweather')

from blueweather import plugin
from blueweather.plugin import types
import blueweather.weather.status
import blueweather.weather.weather
import blueweather.config


plugin_manager = plugin.PluginManager()
status = blueweather.weather.status.Status()
weather = blueweather.weather.weather.Weather()
config = blueweather.config.WebConfig(os.path.join(data_dir, 'config.yaml'))


def load_status() -> dict:
    """
    Request the plugins for an update to status, and return the updated status
    """
    plugin_manager.call(types.WeatherPlugin,
                        types.WeatherPlugin.on_status_request,
                        call_time=5)
    return status.getStatus()


def load_weather() -> dict:
    plugin_manager.call(types.WeatherPlugin,
                        types.WeatherPlugin.on_weather_request,
                        call_time=1)
    return weather.getWeather()
