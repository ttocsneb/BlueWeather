from blueweather import plugin
from blueweather.plugin import types
from blueweather import weather

plugin_manager = plugin.PluginManager()
status = weather.status.Status()


def load_status() -> dict:
    """
    Request the plugins for an update to status, and return the updated status
    """
    plugin_manager.call(types.WeatherPlugin,
                        types.WeatherPlugin.on_status_request)
    return status.getStatus()
