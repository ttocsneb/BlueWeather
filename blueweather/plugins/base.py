import abc

from marshmallow import Schema

from typing import List, Tuple, Dict


class App(metaclass=abc.ABCMeta):
    """
    Tells Blueweather where the Django App lives
    """

    @property
    @abc.abstractmethod
    def app_name(self) -> str:
        """
        Get the name of the app. This should be the package where the app lives
        """


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

        :return: converted value (if the conversion is not available, return
            None)
        """
