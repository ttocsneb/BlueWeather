import logging

from marshmallow import ValidationError

from django.conf import settings

from blueweather.plugins import Plugins
from blueweather.plugins.manager import Plugin

from blueweather.plugins.apps.config import Settings

from . import interface

from typing import List


def initialize() -> List[Plugin]:
    """
    Initialize all the configs

    For each config, make sure that the settings object is correctly
    implemented, the settings exist, and are properly migrated

    :return: list of ready configs
    """
    logger = logging.getLogger(__name__)
    plugins: Plugins = settings.PLUGINS

    ready_settings = []

    configs: dict = settings.CONFIG.apps.settings

    for config in plugins.configs:
        plugin: Settings = config.plugin
        configs.setdefault(plugin.label, {})
        version = configs[plugin.label].get('version', 0)
        if plugin.version > version:
            logger.info(
                "Migrating settings for %s (%s -> %d)",
                repr(plugin.label),
                version,
                plugin.version
            )
            try:
                configs[plugin.label] = plugin.migrate(
                    configs[plugin.label],
                    version
                )
                configs[plugin.label]['version'] = plugin.version
                settings.CONFIG.modified = True
            except Exception:
                logger.exception("Could not migrate %s", repr(plugin.label))
        elif plugin.version < version:
            logger.warn(
                "The saved settings is newer than expected for %s",
                repr(plugin.label)
            )
        ready_settings.append(config)
    return ready_settings


def get_settings_plugin(app: str) -> Plugin:
    """
    Get the settings object for an app

    :return: plugin
    """
    plugins: Plugins = settings.PLUGINS
    for config in plugins.configs:
        plugin: Settings = config.plugin
        if plugin.label == app:
            return config
    raise LookupError


def get_settings_interfaces() -> dict:
    """
    Get the settings interfaces

    :return: all app settings interfaces

    :raise ValueError: if the app's settings object is not an instance
        of :class:`~blueweather.plugins.apps.config.Settings`
    :raise marshmallow.ValidationError: if the settings interface is invalid
    """
    plugins: Plugins = settings.PLUGINS

    def validate(config: Plugin):
        conf: Settings = config.plugin
        label = conf.label

        try:
            return interface.validate_interface(conf.get_interface())
        except ValidationError as error:
            logging.getLogger(__name__).exception(
                "Could not validate interface for '%s'",
                label
            )
            return {
                'error': 'app improperly configured',
                'validate': error.normalized_messages()
            }

    return dict(
        (
            conf.plugin.label.replace('.', '-'),
            validate(conf)
        )
        for conf in plugins.configs
    )


def get_settings(app: str) -> dict:
    """
    Get the settings for an app

    :param app: name of the app

    :return: current settings for the app

    :raise LookupError: if the app doesn't exist
    :raise marshmallow.ValidationError: if the settings aren't valid
    """

    config = get_settings_plugin(app)
    obj: Settings = config.plugin
    label = obj.label

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

    config = get_settings_plugin(app)
    obj: Settings = config.plugin
    label = obj.label

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
