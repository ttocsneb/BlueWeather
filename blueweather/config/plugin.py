from collections import MutableMapping, Mapping, MutableSequence

from blueweather import variables
from blueweather.plugin.types import SettingsPlugin


class NoSettingsPath(Exception):
    pass


class PluginConfigManager(MutableMapping):

    plugin_name = 'plugin'

    def __init__(self, plugin: SettingsPlugin, name: str):

        self.__plugin = plugin
        self._name = name

        self.__config_data = dict()

        self.__preprocessor_setters = dict()
        self.__preprocessor_getters = dict()

    def get_all_data(self, error_on_path=False, incl_defaults=True):
        try:
            data = variables.config[self.__class__.plugin_name][self._name]
        except:
            if error_on_path:
                raise NoSettingsPath()

            data = dict()

        if incl_defaults:
            defaults = self.__plugin.get_settings_defaults()

            for key, val in defaults.items():
                if key not in data:
                    data[key] = val

        return data

    def _load(self):
        """
        Load the plugin settings
        :returns whether the plugin had a migration:
        """
        migrated = False
        self.__config_data = self.__plugin.on_settings_load()

        # migrate the config
        version = self.get_all_data(incl_defaults=False).get(
            self.__plugin.config_version_key)
        if self.__plugin.get_settings_version() is not version:
            migrated = True
            self.__plugin.on_settings_migrate(
                self.__plugin.get_settings_version(), version)

        # Get the getters and setters
        self.__preprocessor_getters, self.__preprocessor_setters = \
            self.__plugin.get_settings_preprocessors()

        # Let the plugin know that the settings have been initialized.
        self.__plugin.on_settings_initialized()

        return migrated

    def _save(self):
        """
        Save the plugin settings
        """

        to_persist = self.__plugin.on_settings_save(self.__config_data)
        variables.config[self.__class__.plugin_name][self._name] = to_persist

    # MutableMapping functions

    @property
    def data(self):
        return self.__config_data

    def __contains__(self, item):
        return item in self.data

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        if key in self.__preprocessor_getters:
            return self.__preprocessor_getters[key](self.data[key])
        return self.data[key]

    def __setitem__(self, key, value):
        if key in self.__preprocessor_setters:
            self.data[key] = self.__preprocessor_setters[key](value)
            return
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        return dict(self.items()) == dict(other.items())

    def __iter__(self):
        return iter(self.data)

    def keys(self):
        return self.data.keys()

    def items(self):
        return {key: self[key] for key in self.keys()}.items()

    def values(self):
        return [self[key] for key in self.keys()]


class PluginConfigManagerManager(MutableSequence):
    """
    The manager for the manager.
    """

    def __init__(self):

        self._plugin_managers = list()

    def createPluginManager(self, plugin: SettingsPlugin, name: str):
        """
        Create a new plugin manager for a plugin

        :returns: the created plugin_manager
        """
        plugin_manager = self.get_from_name(name)
        if self.get_from_name(name) is not None:
            return plugin_manager

        plugin_manager = PluginConfigManager(plugin, name)
        self.addPluginManager(plugin_manager)
        return plugin_manager

    def addPluginManager(self, plugin_manager: PluginConfigManager):
        """
        Add an already existing plugin manager to the plugin manager manager.
        """
        self._plugin_managers.append(plugin_manager)

    def save(self):
        """
        Save all the plugin configuration settings
        """
        for config in self:
            config._save()

    def load(self):
        """
        Load all the plugin configuration settings
        """
        changed = False

        for config in self:
            if config._load():
                changed = True

        if changed:
            variables.config.save()

    def get_from_name(self, name: str, default=None):
        for manager in self:
            if manager._name == name:
                return manager
        return default

    # MutableMapping functions

    @property
    def data(self):
        return self._plugin_managers

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def insert(self, index, value):
        self.data.insert(index, value)
