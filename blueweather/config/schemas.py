"""
The Schemas for the settings file.

This module contains all schemas for exporting and importing setings to the
config.yml file.
"""

from marshmallow import Schema, fields, post_load, pre_load
from . import custom_fields, objects, migrations


class ApiKey(Schema):
    """
    The APi Key Schema
    """
    key = custom_fields.APIKey()
    permissions = fields.List(fields.String())

    @post_load
    def load_apikey(self, data, **kwargs):
        return objects.ApiKey(**data)


class SidebarItem(Schema):
    """
    The Sidebar Schema
    """
    category = fields.String()
    '''The category for the Sidebar Item'''
    value = fields.String()
    '''The value for the Sidebar Item'''


class Web(Schema):
    """
    The Web Schema
    """
    debug = fields.Boolean()
    '''Whether the server starts in debug mode'''
    time_zone = fields.String()
    '''The time zone of the server'''
    allowed_hosts = fields.List(fields.String())
    '''The allowed hosts that the server will listen on.'''
    database = custom_fields.Database()
    '''The server database: :class:`custom_fields.Database`'''
    secret_key = fields.String()
    '''The server's secret key'''
    sidebar = custom_fields.NamedList(
        fields.Nested(SidebarItem), 'category', 'value'
    )
    '''The sidebar settings: :class:`custom_fields.NamedList`
    :class:`SidebarItem`'''
    api_keys = fields.Dict(fields.String(), fields.Nested(ApiKey))
    '''The api keys that allow access to the api without needing to be logged
    in'''

    @post_load
    def make_web(self, data: dict, **kwargs):
        return objects.Web(**data)


class System(Schema):
    """
    The System Schema
    """
    commands = fields.Dict(fields.String(), fields.String())
    '''A list of system commands'''

    @post_load
    def make_system(self, data: dict, **kwargs):
        return objects.System(**data)


class Plugins(Schema):
    """
    The Plugin Schema
    """
    weather_driver = fields.String()
    '''The weather driver extension'''
    disabled = fields.List(fields.String())
    '''A list of disabled plugins'''

    @post_load
    def make_plugins(self, data: dict, **kwargs):
        return objects.Plugins(**data)


class Apps(Schema):
    """
    The Apps Schema
    """
    settings = fields.Dict(
        fields.String(),
        fields.Dict(fields.String())
    )
    '''A dictionary of plugin settings'''

    @post_load
    def make_apps(self, data: dict, **kwargs):
        return objects.Apps(**data)


class Config(Schema):
    """
    The base Config Schema
    """
    web = fields.Nested(Web)
    ''':class:`Web`'''
    system = fields.Nested(System)
    ''':class:`System`'''
    plugins = fields.Nested(Plugins)
    ''':class:`Plugins`'''
    version = fields.Integer()
    '''The version of settings'''

    @pre_load
    def migrate(self, data: dict, **kwargs) -> dict:
        """
        Migrate the Config from previous versions
        """
        settings, migrated = migrations.migrate_settings(data)
        self._migrated = migrated
        return settings

    @post_load
    def make_config(self, data: dict, **kwargs):
        config = objects.Config(**data)
        if self._migrated:
            config.modified = True
        return config
