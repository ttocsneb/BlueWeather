import abc

from marshmallow import Schema


class Plugin(metaclass=abc.ABCMeta):
    """
    The base plugin configuration.

    All Plugins should implement this extension
    """

    @abc.abstractmethod
    def get_plugin_name(self):
        """
        Get the human readable name of the plugin
        """

    @abc.abstractmethod
    def get_plugin_description(self):
        """
        Get the description for the plugin
        """

    def get_plugin_author(self):
        """
        Get the Author(s) of the plugin
        """
        return None

    def get_plugin_url(self):
        """
        Get the plugin's url
        """
        return None


class Startup(metaclass=abc.ABCMeta):
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


class API(metaclass=abc.ABCMeta):
    """
    An Extension that allows for ReST API calls
    """

    @abc.abstractmethod
    def get_api_urlpatterns(self):
        """
        get a list of url patterns for the api

        the patterns should use `django.urls` patterns such as path

        example:

        >>> from django.urls import path
        >>> from . import views
        >>> pattern = [
                path("data/", views.data, name="data")
            ]

        The namespace of the urls will be api:<extensionName>, so the name of
        a path will be api:<extensionName>:<pathName>

        Using the example above, assuming the extension name is 'extension',
        the full url name of data will be `api:extension:data`
        """


class Settings(metaclass=abc.ABCMeta):
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

    def on_settings_migrate(self, version: int, settings: dict) -> dict:
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


class Weather(metaclass=abc.ABCMeta):
    """
    Plugin that Collects the weather
    """

    @abc.abstractmethod
    def on_weather_request(self) -> dict:
        """
        Collect the current weather

        This should be returned as a dictionary of tuples. Each tuple
        contains the unit and value in that order:
            >>> {
                    "temperature": ("celsius", 25.3),
                    "wind_speed": ("meter/second", 5.2)
                }

        While a unit does not need to be a standardized unit, it is
        important that it is a unit accessable to conversions through the
        UnitConversion extension.

        The following list contains units that are garanteed to be convertable

        temperature: celsius
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

        :return dict(str name, (str type, float value))
        """


class UnitConversion(metaclass=abc.ABCMeta):
    """
    Plugin that can facilitate conversions

    Blueweather is bundled with a conversion plugin for metric and imperial
    units.

    It will most likely not be necessary to create a custom UnitConversion
    Extension, but it is here just in case.
    """

    @abc.abstractmethod
    def get_conversion_types(self) -> list:
        """
        Get a list of available conversions in the form of tuples

        :return list( (str from_type, str to_type) ):
        """

    @abc.abstractmethod
    def on_request_conversion(self, data: float, from_type: str, to_type: str
                              ) -> float:
        """
        Convert from one type to another. If you cannot convert from or to the
        requested types, then return None

        When converting values, the first successful conversion will stop
        """
