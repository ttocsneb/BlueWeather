import os
from pathlib import Path
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
        types.Requests
    ]

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._manager = yapsy.PluginManager.PluginManager()

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

    def activatePlugins(self):

        plugins = ''
        count = 0

        for pluginInfo in self._manager.getPluginsOfCategory(
                types.BlueWeatherPlugin.__name__):
            plugins += '\n| {name} ({version}) = {path}'.format(
                name=pluginInfo.name, version=pluginInfo.version,
                path=pluginInfo.path)
            count += 1
            pluginInfo.plugin_object.activate()
            self._loadPluginData(pluginInfo)

        self._logger.info('%d plugin(s) registered with the system: %s',
                          count, plugins)

    def call(self, plugin: type, func: callable, *args,
             **kwargs):
        """
        Call a mixin function on all plugins.  ``plugin`` should be a class
        from :module:``~blueweather.plugin.types`` and ``func`` should be a
        function from the ``plugin`` class

        :param type plugin: Mixin type

        :param callable func: function from ``plugin``

        :param tuple *args: args for the function

        :param dict **kwargs: keword args for the function
        """
        func_name = func.__name__
        plugin_name = plugin.__name__

        self._logger.debug("calling %s.%s()", plugin_name, func_name)

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
