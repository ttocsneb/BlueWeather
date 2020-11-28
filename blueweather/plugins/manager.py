import logging
import collections.abc

from django.apps import AppConfig, apps

from typing import List


class Plugin:
    """
    A single plugin object

    Contains information about the plugin

    :param plugin: plugin object
    :param app: app the plugin belongs to
    """
    def __init__(self, plugin: object, app: AppConfig):
        self.plugin = plugin
        self.app = app

    def call(self, func: str, *args, **kwargs):
        """
        Call a function in the plugin

        :param func: function name to call
        """
        return getattr(self.plugin, func)(*args, **kwargs)

    def __repr__(self):
        return "<{}: {} from {}>".format(
            self.__class__.__name__,
            repr(self.plugin.__class__.__name__),
            repr(self.app.label)
        )


class PluginManager(collections.Sized, collections.Iterable):
    """
    The base class for the plugin manager
    """
    def __init__(self, name: str, loader: callable):
        self.name = name
        self.loader = loader
        self.plugins: List[Plugin] = []
        self.logger = logging.getLogger(__name__)

    def load(self):
        """
        Load the plugins
        """
        self.plugins.clear()
        for app in apps.get_app_configs():
            plugins = self.loader(app)
            if not isinstance(plugins, list):
                plugins = [plugins]
            for plugin in plugins:
                p = Plugin(plugin, app)
                self.plugins.append(p)
                self.logger.info("Loaded %s", p)

    def map(self, func: callable):
        """
        Map a function to all the plugins this manager manages

        :param func: function to call on each plugin
        """
        for plugin in self:
            try:
                yield func(plugin)
            except Exception:
                self.logger.exception(
                    "An exception was raised while mapping %s",
                    plugin
                )

    def mapCall(self, func_name, *args, **kwargs):
        """
        Map a function to all the plugins this manager manages

        :param func_name: name of the function to call
        """
        return self.map(lambda plugin: plugin.call(func_name, *args, **kwargs))

    def __len__(self):
        return len(self.apps)

    def __iter__(self):
        return iter(self.apps)


class DriverManager(PluginManager):
    """
    A plugin manager for a single plugin

    :param app: app to load the plugin from
    :param loader: loader
    """
    def __init__(self, app: str, name: str, loader: callable):
        super().__init__(name, loader)
        self.app = app

    def load(self):
        """
        Load the plugins
        """
        self.plugins.clear()
        app = apps.get_app_config(self.app)
        plugin = self.loader(app)
        if not plugin:
            self.logger.warn(
                "Could not load %s driver from %s",
                self.name,
                repr(self.app)
            )
            return
        p = Plugin(plugin, app)
        self.plugins.append(p)
        self.logger.info("Loaded %s", p)
