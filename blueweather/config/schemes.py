from marshmallow import Schema, fields, post_dump, post_load, pre_dump

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


class WebSchema(Schema):
    static_url = fields.String()
    databases = fields.Dict(fields.String(), customFields.Database())
    password_validation = customFields.NamedList(
        fields.Nested(PasswordValidator), "name", "options", dict_value=True
    )
    allowed_hosts = fields.List(fields.String(), allow_none=True)

    get_object = pre_dump(fn=customFields.get_object)
    strip_defaults = post_dump(fn=customFields.strip_defaults)

    @post_load
    def makeWeb(self, data, **kwargs):
        return objects.Web(**data)


class ConfigSchema(Schema):
    secret_key = fields.String()
    debug = fields.Boolean()
    web = fields.Nested(WebSchema)
    time_zone = fields.String()

    get_object = pre_dump(fn=customFields.get_object)
    strip_defaults = post_dump(fn=customFields.strip_defaults)

    @post_load
    def makeConfig(self, data, **kwargs):
        return objects.Config(**data)
