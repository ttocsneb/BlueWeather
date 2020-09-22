from marshmallow import Schema
from stevedore.extension import Extension, ExtensionManager
from stevedore.dispatch import DispatchExtensionManager
from stevedore import EnabledExtensionManager

from blueweather.config import Config

from typing import List, Dict, Set, Tuple

prettyNames = {
    "blueweather.plugins.plugin": "Plugin-Info",
    "blueweather.plugins.weather": "Weather",
    'blueweather.plugins.django': "Web-App",
    'blueweather.plugins.startup': "Startup",
    'blueweather.plugins.settings': "Settings",
    'blueweather.plugins.unitconv': "Unit-Conversion",
    'blueweather.plugins.api': "ReST-API"
}
builtins = [
    'imperialConverter',
    'metricConverter',
    'dummyWeather'
]


def strip_name(tup: tuple):
    return map(lambda x: x[1], tup)


class Plugin:
    """
    Get Plugin Info
    """
    @staticmethod
    def get_plugin_name(ext: Extension) -> str:
        """
        Get the human readable name of the plugin

        :param ext: extension

        :return: plugin name
        """
        return ext.obj.get_plugin_name()

    @staticmethod
    def get_plugin_description(ext: Extension) -> str:
        """
        Get the human readable description of the plugin

        :param ext: extension

        :return: plugin description
        """
        return ext.obj.get_plugin_description()

    @staticmethod
    def get_plugin_author(ext: Extension) -> List[str]:
        """
        Get the authors of the plugin

        :param ext: extension

        :return: plugin authors
        """
        return ext.obj.get_plugin_author()

    @staticmethod
    def get_plugin_url(ext: Extension) -> str:
        """
        Get the url for the plugin

        :param ext: extension

        :return: plugin url
        """
        return ext.obj.get_plugin_url()


class Startup:
    """
    Send messages to plugins on startup
    """
    @staticmethod
    def on_startup(man: EnabledExtensionManager):
        """
        Send a message to all the plugins that the server has started.

        :param man: startup extension manager
        """
        for ext in man.extensions:
            ext.obj.on_startup()


class API:
    """
    Get API Configurations from plugins.
    """

    @staticmethod
    def allApiPatterns(man: ExtensionManager) -> list:
        """
        Get all the API patterns for each api extension

        :param man: API Extension Manager

        :return: list of api patterns
        """
        patterns = list()
        for ext in man.extensions:
            patterns.extend(API.get_api_urlpatterns(ext))
        return patterns

    @staticmethod
    def get_api_urlpatterns(ext: Extension) -> (str, list):
        """
        Get the API Patterns for an extension

        :param ext: extension

        :return: API Patterns
        """
        return ext.obj.get_api_urlpatterns()


class Settings:
    """
    Manage plugins' settings
    """

    @staticmethod
    def load_settings(man: EnabledExtensionManager, config: Config):
        """
        Load the plugins' settings from the supplied config

        All the plugins' settings will be processed and loaded into memory.

        .. note::

            If any changes were made while loading the settings,
            :code:`config.modified` will be set.

        :param man: Settings Extension Manager
        :param config: configuration
        """

        for ext in man.extensions:
            if ext.name not in config.plugins.settings:
                config.plugins.settings[ext.name] = dict()
            
            # Migrate the settings
            settings = config.plugins.settings[ext.name]
            migration, changed = Settings.settings_migrate(ext, settings)
            config.plugins.settings[ext.name] = migration
            if changed:
                config.modified = True

            # Deserialize the settings
            Settings.settings_deserialize(ext, migration)
        
        # After all the settings have been loaded, notify the extensions that
        # the settings have been loaded
        for ext in man.extensions:
            Settings.on_settings_initialized(ext)

    
    @staticmethod
    def unload_settings(man: EnabledExtensionManager, config: Config):
        """
        Unload the plugins' settings to the supplied config.

        The settings stored in memory will be processed and dumped into the supplied config.

        :param man: Settings Extension Manager
        :param config: configuration
        """

        for ext in man.extensions:
            # Serialize the settings
            settings = config.plugins.settings[ext.name]
            serialized = Settings.settings_serialize(ext, settings)

            # Apply the settings
            config.plugins.settings[ext.name] = serialized


    @staticmethod
    def settings_serialize(ext: Extension, settings: dict) -> dict:
        """
        Serialize an extension's settings

        This serializes the extensions local settings, and returns it

        :param ext: extension
        :param setings: saved settings

        :return: serialized settings
        """
        key = ext.obj.config_version_key
        try:
            version = int(settings.get(key, 0))
        except ValueError:
            version = 0
        
        config = ext.obj.settings_serialize(ext.obj._settings)
        config[key] = version

        return config

    @staticmethod
    def settings_deserialize(ext: Extension, settings: dict):
        """
        Deserialize the settings of an extension.

        :param ext: extension
        :param settings: saved settings
        """
        key = ext.obj.config_version_key

        temp = dict(settings)
        if key in temp:
            del temp[key]
        deserialized = ext.obj.settings_deserialize(temp)

        ext.obj._settings = deserialized

    @staticmethod
    def settings_migrate(ext: Extension, settings: dict) -> dict:
        """
        Migrate the settings of the extension

        :param ext: extension
        :param settings: saved settings

        :return: migrated settings
        """
        key = ext.obj.config_version_key
        try:
            version = int(settings.get(key, 0))
        except ValueError:
            version = 0
        
        temp = dict(settings)
        if key in temp:
            del temp[key]

        migration = ext.obj.settings_migrate(version, temp)
        migration[1][key] = migration[0]

        return migration[1], migration[2]

    @staticmethod
    def on_settings_initialized(ext: Extension):
        """
        Send a message to the extension that the settings have been initialized

        :param ext: extension
        """
        ext.obj.on_settings_initialized()


class Weather:
    """
    Get the weather from the weather driver
    """

    @staticmethod
    def on_weather_request(ext: Extension) -> dict:
        """
        request the weather from the weather driver

        :param ext: driver

        :return: weather data
        """
        return ext.obj.on_weather_request()


class UnitConversion:
    """
    Convert diffent units of measurement
    """

    @staticmethod
    def conversions(man: DispatchExtensionManager) -> Dict[str, Set[str]]:
        """
        Get all the basic conversions

        :param man: UnitConversion Extension Manager

        :return: Possible Conversions
        """
        units = dict()
        for name, conversions in man.map(
                lambda *args, **kwargs: True,
                UnitConversion.get_conversion_types):
            if conversions is None:
                continue
            for from_type, to_type in conversions:
                if from_type not in units:
                    units[from_type] = set()
                units[from_type].add(to_type)
        return units

    @staticmethod
    def all_conversions(man: DispatchExtensionManager = None,
                        units: Dict[str, Set[str]] = None) -> Dict[str, Set[str]]:
        """
        Get all the possible conversions

        This finds all the possible conversions by using recursive conversions

        :param man: UnitConversion Extension Manager
        :param units: All the basic conversions

        :return: All the possible conversions
        """
        if units is None:
            units = UnitConversion.conversions(man)
        # Add secondary conversions (Conversions that can be made by
        # converting a conversion)
        for k, v in units.items():
            for u in v:
                if u in units:
                    v.union(units[u])
        return units

    @staticmethod
    def convert(man: DispatchExtensionManager, data: float, from_type: str,
                to_type: str) -> Tuple[List[str], float]:
        """
        Convert from one type to another

        :param man: UnitConversion Extension Manager
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: name(s) of the extensions that performed the conversion, and the converted value
        """
        units = UnitConversion.conversions(man)

        if from_type not in units:
            raise KeyError("%s can not be converted to another type" %
                           from_type)
        to_types = units[from_type]

        def conv(d, from_t, to_t) -> (str, float):
            for ext in man.extensions:
                if not UnitConversion.on_request_conversion_check(
                        ext, d, from_t, to_t):
                    continue
                val = ext.obj.request_conversion(d, from_t, to_t)
                if val is not None:
                    return ext.name, val
            raise KeyError("%s can not be converted to %s" % (from_t, to_t))

        # It is a simple conversion, so we can convert directly
        if to_type in to_types:
            return conv(data, from_type, to_type)

        # It may be a complex (two part conversion) so we will need to see if
        # it is possible to convert

        from_types = set()
        for k, v in units.items():
            if to_type in v:
                from_types.add(k)

        mid_type = None
        for t in units[from_type]:
            if t not in from_types:
                continue
            # Make the Middle conversion
            mid_type = t
            name1, data = conv(data, from_type, mid_type)

        if mid_type is None:
            raise KeyError("%s can not be converted to %s" %
                           (from_type, to_type))
        # Make final conversion
        name2, data = conv(data, mid_type, to_type)
        return (name1, name2), data

    @staticmethod
    def get_conversion_types(ext: Extension) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Get the types that an extension can convert

        :param ext: extension

        :return: extension name, and possible conversions
        """
        return ext.name, ext.obj.get_conversion_types()

    @staticmethod
    def on_request_conversion_check(ext: Extension, data: float,
                                    from_type: str, to_type: str) -> bool:
        """
        Check if a conversion can be performed

        :param ext: extension
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: True if the conversion is possible
        """
        _, types = UnitConversion.get_conversion_types(ext)
        return next(
            (True for t in types if t[0] == from_type and t[1] == to_type),
            False
        )

    @staticmethod
    def request_conversion(ext: Extension, data: float, from_type: str,
                              to_type: str) -> (str, float):
        """
        Request a conversion to be made

        :param ext: extension
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: the name of the extension, and the converted value
        """
        data = ext.obj.request_conversion(data, from_type, to_type)
        if data is not None:
            return ext.name, data
