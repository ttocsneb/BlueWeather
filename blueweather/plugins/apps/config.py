"""
The Settings Object allows for apps to integrate with settings for blueweather

The settings are very restrictive on what can be used for settings

To create a settings object, place your Settings class in the :code:`config.py`
module

.. code-block:: python

    class MySettings(Settings):
        version = 1

        def get_interface(self):
            return {}

        def migrate(self, data, version):
            return data

"""
import abc
import logging

from django.conf import settings
from django.apps import AppConfig

from marshmallow import ValidationError

from blueweather.config import interface

from .. import utils


class Settings(metaclass=abc.ABCMeta):
    """
    The Settings object that is defined in the AppConfig

    :param app_label: label of the app
    """

    def __init__(self, app_label: str):
        self.__app_name = app_label

    @property
    def label(self):
        """
        Name of the settings label
        """
        return self.__app_name

    @abc.abstractmethod
    def get_interface(self) -> dict:
        """
        Get the settings interface.

        The settings interface is a definition of what settings are available
        to the api and how they should appear on the settings page.

        .. note::

            This enforces the given settings. This means that the api will
            fail if the do not match what is given in the interface.

        The interface should be structured as follows (using typescript as a
        schema language)

        .. code-block:: ts

            interface Choice {
                key: string
                value: string
                enabled?: boolean
            }

            interface SettingItem {
                name: string,
                type: 'number' | 'select' | 'text' | 'radio' | 'bool'
                default?: string
                enabled?: boolean
                options?: {
                    precision?: number
                    range?: [number, number]
                    hint?: string
                    choices?: Array<Choice>
                    multiple?: boolean
                }
            }

            interface Item {
                type: 'divider' | 'header' | 'label' | 'info' | 'setting'
                value: string
            }

            interface GroupItem {
                type: 'group'
                value: Item | GroupItem
            }

            interface Interface {
                settings: Array<SettingItem>
                items: Array<Item | GroupItem>
            }

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

    @abc.abstractmethod
    def ready(self):
        """
        Called when the settings are ready

        :param config: config
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

    @property
    def config(self) -> dict:
        """
        Get the app's settings

        :return: settings
        """
        return settings.CONFIG.apps.settings[self.__app_name]

    @config.setter
    def config(self, value: dict):
        """
        Set the app's settings

        :param value: new settings
        """
        settings.CONFIG.apps.settings[self.__app_name] = value
        settings.CONFIG.modified = True


def getSettings(config: AppConfig) -> Settings:
    """
    Get the settings from the config

    :param config: app config

    :return: settings
    """
    module = utils.load_app_module(config, 'config')
    if not module:
        return []

    try:
        s = next(
            s for s in utils.find_members(module)
            if issubclass(s[1], Settings) and s[1] != Settings
        )
    except StopIteration:
        return []

    try:
        return s[1](config.label)
    except Exception:
        logging.getLogger(__name__).exception(
            "Could not load %s for %s app",
            s[1],
            repr(config.label)
        )
        return []
