from django.apps import registry
from django.conf import settings

from blueweather.config.interface import validate_interface


def get_settings_interface(app: str) -> dict:
    """
    Get the settings interface

    :param app: name of the app

    :return: interface for the app

    :raise KeyError: if the app doesn't exist or doesn't have a settings
    interface

    :raise marshmallow.ValidationError: if the settings interface is invalid
    """

    if not registry.apps.is_installed(app):
        raise KeyError

    config = registry.apps.get_app_config(app)

    if hasattr(config, 'settings'):
        return validate_interface(config.settings)
    raise KeyError


def get_settings(app: str) -> dict:
    """
    Get the settings for an app

    :param app: name of the app

    :return: current settings for the app

    :raise: KeyError if the app doesn't exist
    """

    if not registry.apps.is_installed(app):
        raise KeyError

    if app not in settings.CONFIG.apps.settings:
        settings.CONFIG.apps.settings[app] = {}

    return settings.CONFIG.apps.settings[app]
