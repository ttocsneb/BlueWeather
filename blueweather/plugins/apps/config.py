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
