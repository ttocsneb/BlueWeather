import logging

from django.apps import registry, AppConfig
from django.conf import settings

from marshmallow import ValidationError

from blueweather.config import interface
from blueweather.plugins.apps import config

from typing import List


def get_settings_conf(conf: AppConfig) -> config.Settings:
    """
    Get the settings from an AppConfig

    :param conf: appConfig

    :return: settings or None
    """
    # Check if the app is already configured
    if hasattr(conf, 'settings_obj'):
        return conf.settings_obj
    # Check if the app has settings
    if not hasattr(conf, 'settings'):
        return None
    # Assert that the settings is a class
    if not isinstance(conf.settings, type):
        logging.getLogger(__name__).warning(
            "'settings' should be a type: '%s'",
            conf.label
        )
    # Assert that the settings is a subclass of the Settings base class
    if issubclass(conf.settings, config.Settings):
        try:
            # configure the settings
            conf.settings_obj = conf.settings(conf.label)
        except Exception:
            logging.getLogger(__name__).exception(
                "Could not initialize %s for '%s'",
                conf.settings,
                conf.label
            )
            conf.settings_obj = None
            return None
        return conf.settings_obj
    logging.getLogger(__name__).warn(
        "'%s:settings' is not subclass of %s",
        conf.label, str(type(config.Settings))
    )


def initialize() -> List[config.Settings]:
    """
    Initialize all the configs

    For each config, make sure that the settings object is correctly
    implemented, the settings exist, and are properly migrated

    :return: list of ready
    """
    logger = logging.getLogger(__name__)

    ready_settings = []

    for conf in registry.apps.get_app_configs():
        app_settings = get_settings_conf(conf)
        # Skip the app if it doesn't have a settings object
        if not app_settings:
            continue

        # Make sure the settings object exists
        if conf.label not in settings.CONFIG.apps.settings:
            settings.CONFIG.apps.settings[conf.label] = {
                'version': 0
            }

        # Make sure the settings are up to date
        conf_settings = settings.CONFIG.apps.settings
        version = conf_settings[conf.label].get('version', 0)
        if app_settings.version > version:
            logger.info(
                "Migrating settings for '%s' (%d -> %d)",
                conf.label,
                version,
                app_settings.version
            )
            # Migrate outdated settings
            try:
                conf_settings[conf.label] = app_settings.migrate(
                    conf_settings[conf.label],
                    version
                )
            except Exception:
                logger.exception("Could not migrate '%s'", conf.label)
            conf_settings[conf.label]['version'] = app_settings.version
            # Mark the settings as out of date
            settings.CONFIG.modified = True
        elif app_settings.version < version:
            logger.warn(
                "The saved settings is newer than expected for '%s'",
                conf.label
            )

        # Let the settings know that everything is ready
        ready_settings.append(app_settings)

    return ready_settings


def get_settings_app(app: str) -> (config.Settings, str):
    """
    Get the Settings object for an app

    :param app: name of the app

    :return: Settings object, app label

    :raise KeyError: if the app doesn't exist or doesn't have a settings object
    :raise ValueError: if the app's settings object is not an instance
        of :class:`~blueweather.plugins.apps.config.Settings`
    """

    conf = registry.apps.get_app_config(app)
    if hasattr(conf, 'settings'):
        return get_settings_conf(conf), conf.label
    raise LookupError


def get_settings_interfaces() -> dict:
    """
    Get the settings interfaces

    :return: all app settings interfaces

    :raise ValueError: if the app's settings object is not an instance
        of :class:`~blueweather.plugins.apps.config.Settings`
    :raise marshmallow.ValidationError: if the settings interface is invalid
    """

    def validate(conf: config.Settings, label: str):
        try:
            return interface.validate_interface(conf.get_interface())
        except ValidationError:
            logging.getLogger(__name__).exception(
                "Could not validate interface for '%s'",
                label
            )
            return {
                'error': 'app improperly configured'
            }

    return dict(
        (
            conf.label.replace('.', '-'),
            validate(get_settings_conf(conf), conf.label)
        )
        for conf in registry.apps.get_app_configs()
        if get_settings_conf(conf)
    )


def get_settings(app: str) -> dict:
    """
    Get the settings for an app

    :param app: name of the app

    :return: current settings for the app

    :raise LookupError: if the app doesn't exist
    :raise marshmallow.ValidationError: if the settings aren't valid
    """

    obj, label = get_settings_app(app)

    if app not in settings.CONFIG.apps.settings:
        settings.CONFIG.apps.settings[label] = {}

    return interface.read_settings(
        obj.interface(),
        settings.CONFIG.apps.settings[label]
    )


def set_setting(app: str, setting: str, value):
    """
    Set a setting for an app

    :param app: name of the app
    :param setting: setting name
    :param value: value to set to

    :raise LookupError: if the app doesn't exist
    :raise KeyError: if the setting isn't valid
    :raise marshmallow.ValidationError: if the value isn't valid
    """

    obj, label = get_settings_app(app)

    if app not in settings.CONFIG.apps.settings:
        settings.CONFIG.apps.settings[label] = {}

    settings.CONFIG.apps.settings[label][setting] = interface.validate_setting(
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
