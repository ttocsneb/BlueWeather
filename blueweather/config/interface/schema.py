from marshmallow import Schema, fields

from . import custom_fields


class Choice(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(missing=True)


class Options(Schema):
    precision = fields.Integer(required=False)
    range = fields.Tuple((fields.Integer(), fields.Integer()), required=False)
    hint = fields.String(required=False)
    choices = fields.Nested(Choice, many=True, required=False)
    multiple = fields.Boolean(required=False)


class SettingItem(Schema):
    name = fields.String(required=True)
    type = custom_fields.Choice(
        ('number', 'select', 'text', 'radio', 'bool'),
        required=True
    )
    default = fields.String(required=False)
    enabled = fields.Boolean(missing=True)
    options = fields.Nested(Options, unknown='EXCLUDE', missing=dict)


choices = ('divider', 'header', 'label', 'info', 'setting', 'group')


class Item(Schema):
    type = custom_fields.Choice(choices)
    value = custom_fields.Typed('type', {
        'group': fields.Nested(lambda: Item())
    }, fields.String(), custom_fields.Choice(choices), required=False)


class Settings(Schema):
    settings = fields.Nested(SettingItem, many=True)
    items = fields.Nested(Item, many=True)
