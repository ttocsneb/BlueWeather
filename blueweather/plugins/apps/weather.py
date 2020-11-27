import abc

from django.apps import AppConfig

from typing import Dict, Tuple

from .. import utils


class Weather(metaclass=abc.ABCMeta):
    """
    Plugin that Collects the weather data
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


def getWeather(config: AppConfig) -> Weather:
    """
    Get the weather from the config

    :param config: app config

    :return: weather
    """
    module = utils.load_app_module(config, 'weather')
    if not module:
        return None

    try:
        return next(
            s[1] for s in utils.find_members(module)
            if isinstance(s[1], Weather)
        )
    except StopIteration:
        return None
