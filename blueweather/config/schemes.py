from marshmallow import Schema, fields, post_load, post_dump, pre_dump

from . import objects


def get_object(self, obj: objects.Config, **kwargs):
    self._obj = obj
    return obj


def strip_defaults(self, data, **kwargs):
    if not hasattr(self, "_obj") \
            or not hasattr(self._obj, "_defaults") \
            or not hasattr(self._obj, "_required"):
        return data
    new_data = dict()
    for k, v in data.items():
        if k in self._obj._required \
                or k not in self._obj._defaults \
                or v != self._obj._defaults[k]:
            new_data[k] = v
            continue
    return new_data


class WebSchema(Schema):
    static_url = fields.String()

    @post_load
    def makeWeb(self, data, **kwargs):
        return objects.Web(**data)


class ConfigSchema(Schema):
    secret_key = fields.String()
    debug = fields.Boolean()
    web = fields.Nested(WebSchema)

    get_object = pre_dump(fn=get_object)
    strip_defaults = post_dump(fn=strip_defaults)

    @post_load
    def makeConfig(self, data, **kwargs):
        return objects.Config(**data)
