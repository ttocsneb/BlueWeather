from blueweather import plugin
from blueweather.plugin import types
from blueweather.weather import status as weatherStatus

plugin_manager = plugin.PluginManager()
status = weatherStatus.Status()


def load_status() -> dict:
    """
    Request the plugins for an update to status, and return the updated status
    """
    plugin_manager.call(types.WeatherPlugin,
                        types.WeatherPlugin.on_status_request,
                        call_time=1)
    return status.getStatus()
