import logging
import sys

from stevedore import DriverManager, EnabledExtensionManager
from stevedore.dispatch import DispatchExtensionManager
from stevedore.extension import Extension, ExtensionManager

from blueweather.config import Config

from . import dao
from .managers.settings import SettingsManager


class ExtensionsSingleton:
    def __init__(self, config: Config, invoke_on_load=False):
        self._logger = logging.getLogger(__name__)

        self.failed_plugins = list()
        self._disabled_plugins = config.extensions.disabled

        self._settings_initialized = False

        def check(ext: Extension):
            return self._check_extension(config, ext)

        self.weather = DriverManager(
            "blueweather.plugins.weather",
            config.extensions.weather_driver,
            on_load_failure_callback=self._on_load_fail
        )
        self.plugins = ExtensionManager(
            "blueweather.plugins.plugin",
            on_load_failure_callback=self._on_load_fail
        )
        self.api = EnabledExtensionManager(
            "blueweather.plugins.api",
            check_func=check,
            on_load_failure_callback=self._on_load_fail
        )
        self.startup = EnabledExtensionManager(
            "blueweather.plugins.startup",
            check_func=check,
            on_load_failure_callback=self._on_load_fail
        )
        self.settings = SettingsManager(
            "blueweather.plugins.settings",
            check_func=check,
            on_load_failure_callback=self._on_load_fail
        )
        self.unitConversion = DispatchExtensionManager(
            "blueweather.plugins.unitconv",
            check_func=check,
            on_load_failure_callback=self._on_load_fail
        )

        if self._logger.isEnabledFor(logging.INFO):
            extensions = self.getAllExtensions()
            for k, v in extensions.items():
                extensions[k] = '\n\t'.join(v.keys())

            extensions = '\n'.join(
                ["%s: \n\t%s" % (k, v) for k, v in extensions.items()]
            )

            self._logger.info("Discovered Extensions: \n%s", extensions)

        if invoke_on_load:
            self.invoke()

    def getPluginList(self):
        extensions = self.getAllExtensions()
        data = dict()

        for name, exts in extensions.items():
            desc = exts['blueweather.plugins.plugin']
            data[name] = {
                'human_name': dao.Plugin.get_plugin_name(desc),
                'description': dao.Plugin.get_plugin_description(desc),
                'author': dao.Plugin.get_plugin_author(desc),
                'url': dao.Plugin.get_plugin_url(desc),
                'entrypoints': [
                    dao.prettyNames[man]
                    for man, ext in exts.items()
                    if man != 'blueweather.plugins.plugin'
                ],
                'builtin': desc.builtin,
                'enabled': name not in self._disabled_plugins,
                'disableable': name != self.weather.extensions[0].name
            }
        return data

    def getAllExtensions(self):
        extensions = dict()

        def collect(man: ExtensionManager):
            for ext in man.extensions:
                if ext.name not in extensions:
                    extensions[ext.name] = dict()
                extensions[ext.name][man.namespace] = ext

        collect(self.plugins)
        collect(self.weather)
        collect(self.startup)
        collect(self.settings)
        collect(self.unitConversion)
        collect(self.api)
        return extensions

    def invoke(self):
        """
        Invoke the classes that have been loaded
        """
        objects = dict()

        def invoke_plugins(plugin: ExtensionManager):
            for ext in plugin.extensions:
                self._invoke_one(ext, objects)

        invoke_plugins(self.plugins)
        invoke_plugins(self.weather)
        invoke_plugins(self.api)
        invoke_plugins(self.startup)
        invoke_plugins(self.settings)
        invoke_plugins(self.unitConversion)

    def _invoke_one(self, extension: Extension, objects: dict):
        if extension.obj is not None:
            return
        extension.builtin = extension.name in dao.builtins
        if extension.plugin in objects:
            extension.obj = objects[extension.plugin]
        else:
            try:
                extension.obj = extension.plugin()
                objects[extension.plugin] = extension.obj
                if extension.name not in self._disabled_plugins:
                    self._logger.info("Loaded Plugin '%s'", extension.name)
            except Exception as exc:
                self._on_load_fail(None, extension, exc)

    def _on_load_fail(self, manager: ExtensionManager, entrypoint: Extension,
                      exception: Exception):
        """
        Called when a plugin fails to load
        """
        self._logger.warning("Unable to load plugin '%s'", entrypoint.name,
                             exc_info=sys.exc_info(), stack_info=True)
        self.failed_plugins.append((entrypoint, exception))

    def _check_extension(self, config: Config, extension: Extension):
        """
        Check if a function should be enabled
        """
        if extension.name in config.extensions.disabled:
            return False
        return True
