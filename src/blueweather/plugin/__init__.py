import os
from pathlib import Path
import time
import logging

import yapsy.PluginManager

from . import types

dirname = os.path.dirname(os.path.relpath(__file__))


class PluginManager:

    plugin_locations = (
        os.path.join(dirname, 'plugins'),
        os.path.join(str(Path.home()), 'blueweather', 'plugins')
    )

    _plugins = [
        types.BlueWeatherPlugin,
        types.StartupPlugin,
        types.RequestsPlugin,
        types.WeatherPlugin
    ]

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._manager = yapsy.PluginManager.PluginManager()

        self._timers = dict()

    def loadPlugins(self):

        paths = ', '.join(self.__class__.plugin_locations)
        self._logger.info("loading plugins from %s", paths)

        self._manager.getPluginLocator().setPluginPlaces(
            self.__class__.plugin_locations)

        # create a plugins dictionary with the `plugin.__name__` as the key
        plugins = {plugin.__name__: plugin
                   for plugin in self.__class__._plugins}
        self._manager.setCategoriesFilter(plugins)

        self._manager.collectPlugins()

    @staticmethod
    def _loadPluginData(plugin: yapsy.PluginInfo):
        from blueweather import variables
        obj = plugin.plugin_object

        log_name = 'blueweather.plugins.' + os.path.basename(plugin.path)
        obj._logger = logging.getLogger(log_name)
        obj._status = variables.status
        obj._weather = variables.weather

        details = plugin.details

        if 'PluginInfo' in details.sections():
            info = details['PluginInfo']
            obj._bundled = True if info.get('Bundled', 'no') == 'yes' \
                else False

    def activatePlugins(self):

        plugins = ''
        count = 0

        for pluginInfo in self._manager.getPluginsOfCategory(
                types.BlueWeatherPlugin.__name__):
            count += 1
            pluginInfo.plugin_object.activate()
            self._loadPluginData(pluginInfo)

            bundled = ''
            if pluginInfo.plugin_object._bundled:
                bundled = '(bundled) '

            plugins += '\n| {name} ({version}) {bundled}= {path}'.format(
                name=pluginInfo.name, version=pluginInfo.version,
                path=pluginInfo.path, bundled=bundled)

        self._logger.info('%d plugin(s) registered with the system: %s',
                          count, plugins)

    def call(self, plugin: type, func: callable, args=None, kwargs=None,
             call_time=0) -> bool:
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
                    getattr(pluginInfo.plugin_object, func_name)(
                        *args, **kwargs)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self._logger.warning("Disabling '%s' due to runtime error",
                                         pluginInfo.name)
                    pluginInfo.plugin_object.deactivate()
        return True
