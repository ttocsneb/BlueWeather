from marshmallow import (Schema, fields, post_dump, post_load, pre_dump,
                         validate)

from . import fields as customFields
from . import objects


class PasswordValidator(Schema):
    name = customFields.ClassString("django.contrib.auth.password_validation")
    options = fields.Dict(fields.String)

    @pre_dump
    def to_lower(self, obj: dict, **kwargs):
        new_data = dict()
        for k, v in obj.items():
            new_data[k.lower()] = v
        return new_data

    @post_load
    def to_upper(self, data: dict, **kwargs):
        new_data = dict()
        for k, v in data.items():
            new_data[k.upper()] = v
        return new_data


class SidebarSchema(Schema):
    category = fields.String()
    value = fields.String()


class WebSchema(Schema):
    static_url = fields.String()
    databases = fields.Dict(fields.String(), customFields.Database())
    password_validation = customFields.NamedList(
        fields.Nested(PasswordValidator), "name", "options", dict_value=True
    )
    allowed_hosts = fields.List(fields.String(), allow_none=True)
    template_globals = fields.Dict(fields.String(), fields.String())

    get_object = pre_dump(fn=customFields.get_object)
    strip_defaults = post_dump(fn=customFields.strip_defaults)

    sidebar = customFields.NamedList(
        fields.Nested(SidebarSchema), "category", "value", value_only=True
    )

    @post_load
    def makeWeb(self, data, **kwargs):
        return objects.Web(**data)


class ExtensionsSchema(Schema):
    weather_driver = fields.String()
    disabled = fields.List(fields.String())
    settings = fields.Dict(fields.String(), fields.Dict(fields.String))

    get_object = pre_dump(fn=customFields.get_object)
    strip_defaults = post_dump(fn=customFields.strip_defaults)

    @post_load
    def makeExtensions(self, data, **kwargs):
        return objects.Extensions(**data)


class CommandsSchema(Schema):
    stop = fields.String()
    restart = fields.String()
    shutdown = fields.String()

    @post_load
    def makeCommands(self, data, **kwargs):
        return objects.Commands(**data)


class ConfigSchema(Schema):
    secret_key = fields.String()
    debug = fields.Boolean()
    web = fields.Nested(WebSchema)
    time_zone = fields.String()
    commands = fields.Nested(CommandsSchema)
    extensions = fields.Nested(ExtensionsSchema)

    get_object = pre_dump(fn=customFields.get_object)
    strip_defaults = post_dump(fn=customFields.strip_defaults)

    @post_load
    def makeConfig(self, data, **kwargs):
        return objects.Config(**data)
