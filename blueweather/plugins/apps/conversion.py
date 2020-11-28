import abc

from django.apps import AppConfig

from typing import List, Tuple

from .. import utils


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


def getConversions(config: AppConfig) -> List[UnitConversion]:
    """
    Get the Conversions from the config

    :param config: app config

    :return: list of conversions
    """
    module = utils.load_app_module(config, 'conversions')
    if not module:
        return []

    return [
        s[1]() for s in utils.find_members(module)
        if issubclass(s[1], UnitConversion)
    ]
