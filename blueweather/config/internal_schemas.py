"""
The internal Schemas for the settings

This module contains all schemas for exporting/import the settings for use
with the settings api.
"""

from marshmallow import Schema, fields, post_load
from . import custom_fields, schemas, objects


class Web(Schema):
    """
    The Internal Web Schema
    """
    debug = fields.Boolean()
    '''Whether the server starts in debug mode'''
    time_zone = fields.String()
    '''The time zone of the server'''
    allowed_hosts = fields.List(fields.String())
    '''The allowed hosts that the server will listen on'''
    database = custom_fields.Database()
    '''The server database'''
    sidebar = fields.List(fields.Nested(schemas.SidebarItem))
    '''The sidebar settings'''
    api_keys = fields.Dict(fields.String(), fields.Nested(schemas.ApiKey))
    '''The api keys that allow access to the api without needing to be logged
    in'''

    @post_load
    def make_web(self, data, **kwargs):
        return objects.Web(**data)


class Config(Schema):
    """
    The base Config Settings Schema
    """
    web = fields.Nested(Web)
    system = fields.Nested(schemas.System)
    plugins = fields.Nested(schemas.Plugins)

    @post_load
    def make_config(self, data, **kwargs):
        return objects.Config(**data)
