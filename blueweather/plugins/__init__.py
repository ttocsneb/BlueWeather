import logging
import sys

from stevedore import DriverManager, EnabledExtensionManager
from stevedore.dispatch import DispatchExtensionManager
from stevedore.extension import Extension, ExtensionManager

from blueweather.config import Config

from . import dao

from typing import Dict, List


class Extensions:
    """
    This is the central manager for all plugins.

    There should only exist one Extensions object which will be held
    in the django settings module.

    You can get the django settings from calling

    .. code-block:: python

        from django.conf import settings
        settings.EXTENSIONS

    """

    def __init__(self, config: Config):
        self._logger = logging.getLogger(__name__)

        self.failed_plugins = list()
        self._disabled_plugins = config.plugins.disabled

        self.__invoked_plugins = dict()

        self.weather = DriverManager(
            "blueweather.plugins.weather",
            config.plugins.weather_driver,
            on_load_failure_callback=self._on_load_fail
        )
        self.unitConversion = DispatchExtensionManager(
            "blueweather.plugins.unitconv",
            check_func=self.is_enabled,
            on_load_failure_callback=self._on_load_fail
        )
        self.apps = EnabledExtensionManager(
            "blueweather.plugins.app",
            check_func=self.is_enabled,
            on_load_failure_callback=self._on_load_fail,
        )

        if self._logger.isEnabledFor(logging.INFO):
            extensions = self.getAllExtensions()
            for k, v in extensions.items():
                extensions[k] = '\n\t'.join(v.keys())

            extensions = '\n'.join(
                ["%s:\n\t%s" % (k, v) for k, v in extensions.items()]
            )

            self._logger.info("Discovered Extensions: \n%s", extensions)

        self.invoke(self.apps)

    def getAllExtensions(self) -> Dict[str, Dict[str, Extension]]:
        """
        Get all the loaded extensions

        :return: dict of plugins -> list of extensions
        """
        plugins = dict()

        def get_manager_extensions(manager: ExtensionManager):
            for name, ext in manager.items():
                if name not in plugins:
                    plugins[name] = dict()
                plugins[name][manager.namespace] = ext

        get_manager_extensions(self.apps)
        get_manager_extensions(self.weather)
        get_manager_extensions(self.unitConversion)

        return plugins

    def invoke_all(self):
        """
        Invoke the extensions that have been loaded
        """
        self.invoke(self.weather)
        self.invoke(self.unitConversion)

    def invoke(self, manager: ExtensionManager):
        for ext in manager:
            self._invoke_one(ext)

    def _invoke_one(self, extension: Extension):
        # Make sure that the extension hasn't already been invoked
        if extension.obj is not None:
            return
        extension.builtin = extension.name in dao.builtins
        # If the class has already been invoked, use the loaded one
        if extension.plugin in self.__invoked_plugins:
            extension.obj = self.__invoked_plugins[extension.plugin]
            return
        try:
            extension.obj = extension.plugin()
            self.__invoked_plugins[extension.plugin] = extension.obj
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

    def is_enabled(self, extension: Extension):
        """
        Check if an extension is disabled

        :param extension: extension to check

        :return: whether the extension is disabled
        """
        if extension.name in self._disabled_plugins:
            return False
        return True
