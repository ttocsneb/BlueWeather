"""
The Settings Object allows for apps to integrate with settings for blueweather

The settings are very restrictive on what can be used for settings

To add the settings to the app, set the :class:`Settings` class to the
:code:`settings` variable in your AppConfig.

.. code-block:: python

    class MySettings(Settings):
        version = 1

        def get_interface(self):
            return {}

        def migrate(self, data, version):
            return data


    class MyConfig(AppConfig):
        name = 'myapp'
        label = 'myapp'

        settings = MySettings

.. note::

    Keep in mind that the :code:`settings` variable must be a class, not an
    object. If you want to use an object instead, set :code:`settings_obj` to
    the object.

"""
import abc

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
        return None

    try:
        return next(
            s[1] for s in utils.find_members(module)
            if isinstance(s[1], Settings)
        )
    except StopIteration:
        return None
