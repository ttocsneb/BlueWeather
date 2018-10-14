import os
from pathlib import Path

# Prevent circular imports from plugin_manager
data_dir = os.path.join(str(Path.home()), '.blueweather')

from blueweather import plugin
import blueweather.weather.status
import blueweather.weather.weather
import blueweather.config


config = blueweather.config.WebConfig(os.path.join(data_dir, 'config.yaml'))
status = blueweather.weather.status.Status()
weather = blueweather.weather.weather.Weather()
plugin_manager = plugin.PluginManager()
