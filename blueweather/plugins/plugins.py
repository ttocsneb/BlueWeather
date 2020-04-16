from yapsy.IPlugin import IPlugin
import logging
from marshmallow import Schema


class ILoggerPlugin(IPlugin):
    """
    A Plugin That supports logging

    Use this to allow logging settings to be controlled in one place
    """

    def __init__(self, name):
        super().__init__()
        self._logger_name = name
        self._logger = logging.getLogger(name)

    def get_logger_name(self):
        return self._logger_name


class IStartupPlugin(IPlugin):
    """
    A Plugin that hooks into the start and stop of the web-app
    """

    def on_startup(self, host: str, port: int):
        """
        Called just before the server is started.
        """
        pass

    def on_after_startup(self):
        """
        Called after the server has started.
        """

    def on_shutdown(self):
        """
        Called just before he server has shutdown
        """


class ISettingsPlugin(IPlugin):
    """
    Be able to interact with the settings for the plugin
    """

    config_version_key = "_version"

    def __init__(self):
        super().__init__()

        self._settings = dict()

    def get_default_settings(self) -> dict:
        """
        Get a dictionary of default settings
        This will be applied to missing keys
        """
        return dict()

    def get_required_settings(self) -> dict:
        """
        Get a list of required settings that should always be in the config
        file
        """
        return list()

    def get_settings_schema(self) -> Schema:
        """
        Get the marshmallow schema for loading and dumping settings

        If none is provided, no processing will be made to the settings
        """
        return None

    def on_settings_migrate(self, version: int, settings: dict):
        """
        Migrate the settings from an older version to the current version

        :param int version: the version of the settings
        :param dict settings: the raw loaded settings

        :return dict: raw settings of the current version
        """
        return settings

    def on_settings_initialized(self):
        """
        Called after the settings have been initialized
        """
        pass


class IWeatherPlugin(IPlugin):
    """
    Plugin that Collects the weather
    """

    def on_weather_request(self) -> dict:
        """
        Collect the current weather

        This should be returned as a dictionary of tuples. Each tuple
        contains the type and value in that order:
            >>> {
                    "temperature": ("temperature", 25.3),
                    "wind_speed": ("speed", 5.2)
                }

        The following is a list of valid types and their unit

        temperatures: celsius
        distance: meter
        mass: kilogram
        time: second
        speed: meter/second
        acceleration: meter/second/second
        force: newton
        pressure: pascal
        energy: joule
        power: watt
        current: ampere
        luminous: candela

        You definitely won't need to use all of them, but they are there for
        conversions

        :return dict(str name, (str type, float value))
        """
        raise NotImplementedError("on_weather_request must be implemented")


class IUnitConversionPlugin(IPlugin):
    """
    Plugin that can facilitate conversions

    Blueweather is (will be) bundled with a conversion plugin for imperial
    """

    def get_conversion_types(self) -> list:
        """
        Get a list of available conversions in the form of tuples

        :return list( (str from_type, str to_type) ):
        """
        raise NotImplementedError("on_weather_request must be implemented")

    def on_request_conversion(self, data: float, from_type: str, to_type: str
                              ) -> float:
        """
        Convert from one type to another. If you cannot convert from or to the
        requested types, then return None

        When converting values, the first successful conversion will stop
        """
        raise NotImplementedError("on_weather_request must be implemented")
