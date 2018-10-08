from blueweather.plugin.types import SettingsPlugin
from . import WebConfig


class NoSettingsPath(Exception):
    pass


class PluginConfigManager:

    def __init__(self, config: WebConfig, plugin: SettingsPlugin, name: str):
        if 'plugin' not in config:
            config['plugin'] = dict()

        self.__config = config['plugin']
        self.__plugin = plugin
        self._name = name

    def get_all_data(self, error_on_path=False, incl_defaults=True):
        try:
            data = self.__config[self._name]
        except:
            if error_on_path:
                raise NoSettingsPath()

            data = dict()

        if incl_defaults:
            defaults = self.__plugin.get_settings_defaults()

            for key, val in defaults.values():
                if key not in data:
                    data[key] = val

        return data
