import os
import time
import logging

import yapsy.PluginManager

from blueweather.config.plugin import PluginConfigManagerManager
from blueweather import variables
from . import types

dirname = os.path.dirname(os.path.relpath(__file__))


class PluginLoader:

    def __init__(self):

        self.plugin = None
        self._object = None

    def load(self, plugin: yapsy.PluginInfo):
        """
        Load all the important variables to the plugin
        """

        self.plugin = plugin
        self._object = plugin.plugin_object

        self._load_base()
        if issubclass(type(self._object), types.WeatherPlugin):
            self._load_weather()
        if issubclass(type(self._object), types.SettingsPlugin):
            self._load_settings()

    def _load_base(self):
        details = self.plugin.details

        # Check if the plugin is a bundled plugin
        if 'PluginInfo' in details.sections():
            info = details['PluginInfo']
            self._object._bundled = \
                True if info.get('Bundled', 'no') == 'yes' else False

        # Create the plugin logger
        log_name = 'blueweather.plugins.' + os.path.basename(self.plugin.path)
        self._object._logger = logging.getLogger(log_name)

        # Create the data folder if it does not yet exist
        if not self._object._bundled:
            if os.path.isdir(self.plugin.path):
                self._object._data_folder = os.path.join(
                    self.plugin.path, 'data')
            else:
                self._object._data_folder = os.path.join(
                    os.path.dirname(self.plugin.path), 'data')

            if not os.path.exists(self._object._data_folder):
                os.mkdir(self._object._data_folder)

    def _load_weather(self):

        # Set the status/weather plugin variables
        self._object._status = variables.status
        self._object._weeather = variables.weather

    def _load_settings(self):

        plugin_manager = \
            variables.config.plugin.createPluginManager(
                self._object, self.plugin.name)
        self._object._settings = plugin_manager


class PluginManager:

    plugin_locations = (
        os.path.join(dirname, 'plugins'),
        os.path.join(variables.data_dir, 'plugins')
    )

    _plugins = [
        types.BlueWeatherPlugin,
        types.StartupPlugin,
        types.RequestsPlugin,
        types.WeatherPlugin,
        types.SettingsPlugin,
        types.TemplatePlugin
    ]

    def __init__(self,):
        self._logger = logging.getLogger(__name__)

        self._manager = yapsy.PluginManager.PluginManager()

        ext_dir = self.__class__.plugin_locations[1]
        if not os.path.exists(ext_dir):
            self._logger.info("Creating Plugin Directory at %s",
                              ext_dir)
            os.makedirs(ext_dir)

        self._timers = dict()

    def loadPlugins(self):

        paths = ', '.join([os.path.abspath(path)
                           for path in self.__class__.plugin_locations])
        self._logger.info("loading plugins from %s", paths)

        self._manager.getPluginLocator().setPluginPlaces(
            self.__class__.plugin_locations)

        # create a plugins dictionary with the `plugin.__name__` as the key
        plugins = {plugin.__name__: plugin
                   for plugin in self.__class__._plugins}
        self._manager.setCategoriesFilter(plugins)

        self._manager.collectPlugins()

    def activatePlugins(self):

        plugins = ''
        count = 0

        loader = PluginLoader()

        for pluginInfo in self._manager.getPluginsOfCategory(
                types.BlueWeatherPlugin.__name__):
            count += 1
            self.activate(pluginInfo)
            loader.load(pluginInfo)

            bundled = ''
            if pluginInfo.plugin_object._bundled:
                bundled = '(bundled) '

            plugins += '\n| {name} ({version}) {bundled}= {path}'.format(
                name=pluginInfo.name, version=pluginInfo.version,
                path=pluginInfo.path, bundled=bundled)

        self._logger.info('%d plugin(s) registered with the system: %s',
                          count, plugins)

        variables.config.load()

    def call(self, plugin: type, func: callable, args=None, kwargs=None,
             call_time=0, return_list=None) -> bool:
        """
        Call a mixin function on all plugins.  ``plugin`` should be a class
        from :module:``~blueweather.plugin.types`` and ``func`` should be a
        function from the ``plugin`` class

        :param type plugin: Mixin type

        :param callable func: function from ``plugin``

        :param tuple args: args for the function

        :param dict kwargs: keword args for the function

        :param float call_time: minimum time between each call in seconds
        """
        func_name = func.__name__
        plugin_name = plugin.__name__

        if not args:
            args = tuple()
        if not kwargs:
            kwargs = dict()

        # Check if the last call of the mixin was too soon
        if call_time > 0:
            if time.time() - self._timers.get(func_name + plugin_name, 0) \
                    < call_time:
                return False
            self._timers[func_name + plugin_name] = time.time()

        self._logger.debug("calling %s.%s()", plugin_name, func_name)

        # Call the the mixin function for each plugin
        for pluginInfo in self._manager.getPluginsOfCategory(plugin_name):
            if pluginInfo.is_activated:
                try:
                    ret = getattr(pluginInfo.plugin_object, func_name)(
                        *args, **kwargs)
                    if return_list is not None:
                        ret.append(ret)
                except:
                    import traceback
                    traceback.print_exc()
                    self._logger.warning("Disabling '%s' due to runtime error",
                                         pluginInfo.name)
                    self.deactivate(pluginInfo)
                    return False
        return True

    @staticmethod
    def activate(plugin: yapsy.PluginInfo):
        """
        Activate a BlueWeather plugin

        :param yapsy.PluginInfo plugin: plugin to activate
        """
        plugin.plugin_object.activate()

    @staticmethod
    def deactivate(plugin: yapsy.PluginInfo):
        """
        Deactivate a BlueWeather plugin

        :param yapsy.PluginInfo plugin: plugin to deactivate
        """
        plugin.plugin_object.deactivate()
