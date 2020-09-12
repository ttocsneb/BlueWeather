from marshmallow import fields, Schema, post_load
from . import fields as customFields
from . import objects


class SidebarSchema(Schema):
    category = fields.String()
    value = fields.String()


class APIKeySchema(Schema):
    key = customFields.APIKey()
    name = fields.String(allow_none=True)
    permissions = fields.List(fields.String())

    @post_load
    def makeAPIKey(self, data, **kwargs):
        return objects.APIKey(**data)


class WebSchema(Schema):
    static_url = fields.String()
    allowed_hosts = fields.List(fields.String(), allow_none=True)
    sidebar = fields.List(fields.Nested(SidebarSchema))
    api_keys = fields.List(fields.Nested(APIKeySchema))

    @post_load
    def makeWeb(self, data, **kwargs):
        return objects.Web(**data)


class ExtensionsSchema(Schema):
    weather_driver = fields.String()
    disabled = fields.List(fields.String())
    settings = fields.Dict(fields.String(), fields.Dict())

    @post_load
    def makeConfig(self, data, **kwargs):
        return objects.Extensions(**data)


class CommandSchema(Schema):
    stop = fields.String()
    restart = fields.String()
    shutdown = fields.String()

    @post_load
    def makeCommands(self, data, **kwargs):
        return objects.Commands(**data)


class ConfigSchema(Schema):
    debug = fields.Boolean()
    time_zone = fields.String()
    commands = fields.Nested(CommandSchema)
    extensions = fields.Nested(ExtensionsSchema)
    web = fields.Nested(WebSchema)

    @post_load
    def makeConfig(self, data, **kwargs):
        return objects.Config(**data)