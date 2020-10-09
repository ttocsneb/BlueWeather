from django.apps import registry
from django.conf import settings

from blueweather.config import interface
from blueweather.plugins.apps import config


def get_settings_obj(app: str) -> config.Settings:
    """
    Get the Settings object for an app

    :param app: name of the app

    :return: Settings object

    :raise KeyError: if the app doesn't exist or doesn't have a settings object
    :raise ValueError: if the app's settings object is not an instance
        of :class:`config.Settings`
    """

    if not registry.apps.is_installed(app):
        raise KeyError

    conf = registry.apps.get_app_config(app)
    if hasattr(conf, 'settings'):
        if not isinstance(conf.settings, config.Settings):
            raise ValueError
        return conf.settings
    raise KeyError


def get_settings_interface(app: str) -> dict:
    """
    Get the settings interface

    :param app: name of the app

    :return: interface for the app

    :raise KeyError: if the app doesn't exist or doesn't have a settings
        interface
    :raise ValueError: if the app's settings object is not an instance
        of :class:`config.Settings`
    :raise marshmallow.ValidationError: if the settings interface is invalid
    """

    return interface.validate_interface(get_settings_obj(app).interface())


def get_settings(app: str) -> dict:
    """
    Get the settings for an app

    :param app: name of the app

    :return: current settings for the app

    :raise: KeyError if the app doesn't exist
    :raise marshmallow.ValidationError: if the settings aren't valid
    """

    obj = get_settings_obj(app)

    if app not in settings.CONFIG.apps.settings:
        settings.CONFIG.apps.settings[app] = {}

    return interface.read_settings(
        obj.interface(),
        settings.CONFIG.apps.settings[app]
    )


def set_setting(app: str, setting: str, value):
    """
    Set a setting for an app

    :param app: name of the app
    :param setting: setting name
    :param value: value to set to

    :raise KeyError: if the app doesn't exist
    :raise marshmallow.ValidationError: if the value isn't valid
    """

    obj = get_settings_obj(app)

    if app not in settings.CONFIG.apps.settings:
        settings.CONFIG.apps.settings[app] = {}

    settings.CONFIG.apps.settings[app][setting] = interface.validate_setting(
        obj.interface(),
        setting,
        value
    )
    settings.CONFIG.modified = True


def revert_settings():
    """
    Revert the changes to what is stored on disk
    """

    settings.CONFIG.load()


def apply_settings():
    """
    Write the modified settings to disk
    """

    settings.CONFIG.save()
