import abc

from marshmallow import Schema

from typing import List, Tuple, Dict


class Plugin(metaclass=abc.ABCMeta):
    """
    The base plugin configuration.

    All Plugins must implement this extension

    It gives usefull information to the user
    about the plugin
    """

    @abc.abstractmethod
    def get_plugin_name(self) -> str:
        """
        Get the human readable name of the plugin

        :return: plugin name
        """

    @abc.abstractmethod
    def get_plugin_description(self) -> str:
        """
        Get the description for the plugin

        :return: plugin description
        """

    def get_plugin_author(self) -> list:
        """
        Get the Author(s) of the plugin

        :return: authors
        """
        return None

    def get_plugin_url(self) -> str:
        """
        Get the plugin's url

        :return: url
        """
        return None


class Startup(metaclass=abc.ABCMeta):
    """
    Gets a message when the server is up and running
    """

    def on_startup(self):
        """
        Called when the server is ready
        """
        pass


class API(metaclass=abc.ABCMeta):
    """
    Allows for custom ReST APIs
    """

    @abc.abstractmethod
    def get_api_urlpatterns(self) -> List[Tuple[str, callable, str]]:
        """
        get a list of url patterns for the api

        the patterns should use `django.urls` patterns such as path

        .. code-block:: python

            from . import views
            return [
                ("data/", views.data, "data")
            ]

        In each path, there are 3 parameters:

        1. endpoint (the url path) "data/" -> `api/pluginName/data`
        2. view (the function that can process the path)
        3. name (the name of the path) "data" -> `api:pluginName:data`

        The namespace of the urls will be `api:<pluginName>`, so the name of
        a path will be `api:<pluginName>:<pathName>` (`api:simplePlugin:data`)

        :return: list of paths
        """


class Settings(metaclass=abc.ABCMeta):
    """
    Be able to interact with the settings for the plugin
    """

    config_version_key = "_version"

    def __init__(self):
        super().__init__()

        self._settings = dict()

    def settings_serialize(self, obj) -> dict:
        """
        Serialize the settings object into a json serializeable dict.

        This must undo whatever settings_deserialize does

        :param obj: settings object

        :return: settings primitives
        """
        return obj

    def settings_deserialize(self, data: dict) -> object:
        """
        Deserialize the settings from a dictionary into a custom settings object.

        By default no changes are made, so the default settings object is a
        dict of primitives.

        I recommend using Marshmallow to deserialize your settings.

        :param data: settings dict

        :return: deserialized settings object
        """
        return data

    def settings_migrate(self, version: int, settings: dict) -> Tuple[int, dict, bool]:
        """
        Migrate the settings from an older version to the current version

        .. note::

            This function is always run, it is your job to determine if a migration is required.

        :param version: the version of the settings
        :param settings: the primative loaded settings

        :return: version, updated settings, and whether the data has been changed
        """
        return version, settings, False

    def on_settings_initialized(self):
        """
        Called after the settings have been initialized

        After this has been called, the settings are garenteed to be available
        in `self._settings` as the deserialized object given by `settings_deserialize()`
        """
        pass


class Weather(metaclass=abc.ABCMeta):
    """
    Plugin that Collects the weather
    """

    @abc.abstractmethod
    def on_weather_request(self) -> Dict[str, Tuple[str, float]]:
        """
        Collect the current weather

        This should be returned as a dictionary of tuples. Each tuple
        contains the unit and value in that order:

        .. code-block:: python

            {
                "temperature": ("c", 25.3),
                "wind_speed": ("m/s", 5.2)
            }

        While a unit does not need to be a standardized unit, it is
        important that it is a unit accessable to conversions through the
        UnitConversion extension. If you choose to use your own custom units,
        it is important that you make those units convertable by supplying your
        own conversion extension.

        The following list contains units that are garanteed to be convertable

        * temperature: c
        * distance: m
        * mass: kg
        * time: s
        * speed: m/s
        * acceleration: m/s/s
        * force: N
        * pressure: Pa
        * energy: J
        * power: W
        * current: A
        * luminous: cd

        .. note::

            units are case-sensitive

        :return: weather data
        """


class UnitConversion(metaclass=abc.ABCMeta):
    """
    An Extension that can facilitate conversions

    This allows for custom conversion between units.
    """

    @abc.abstractmethod
    def get_conversion_types(self) -> List[Tuple[str, str]]:
        """
        Get a list of available conversions in the form of tuples

        Each conversion is in the form: `from_type -> to_type`

        :return: list of conversions
        """

    @abc.abstractmethod
    def conversion_request(self, data: float, from_type: str, to_type: str
                              ) -> float:
        """
        Convert from one type to another.

        When converting values, the first successful conversion will stop

        :param data: value in the unit (`from_type`)
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: converted value (if the conversion is not available, return None)
        """
