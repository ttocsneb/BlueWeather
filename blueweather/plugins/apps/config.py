"""
The Settings Object allows for apps to integrate with settings for blueweather

The settings are very restrictive on what can be used for settings
"""
import abc

from blueweather.config import interface

from marshmallow import ValidationError


class Settings(metaclass=abc.ABCMeta):
    """
    The Settings object that is defined in the AppConfig
    """

    @abc.abstractmethod
    def get_interface(self) -> dict:
        """
        Get the settings interface.

        The settings interface is a definition of what settings are available,
        and how they should appear in the settings page.

        :return: interface
        """

    @abc.abstractmethod
    def migrate(self, data: dict, version: int) -> dict:
        """
        Migrate from an old version of the settings to the current version

        :param data: the old settings
        :param version: the version of the old settings

        :return: the new migrated settings
        """

    @property
    @abc.abstractmethod
    def version(self) -> int:
        """
        The version of the settings
        """

    def interface(self) -> dict:
        """
        The validated settings interface

        :return: validated interface

        :raise marshmallow.ValidationError: if the interface is invalid
        """
        if hasattr(self, '_interface'):
            return self._interface
        try:
            self._interface = interface.validate_interface(
                self.get_interface()
            )
            return self._interface
        except ValidationError as error:
            raise SyntaxError from error
