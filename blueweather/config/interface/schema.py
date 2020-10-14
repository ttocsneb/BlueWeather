from marshmallow import Schema, fields, validate

from . import custom_fields


class Choice(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(missing=True)


class SettingItem(Schema):
    name = fields.String(required=True)
    type = fields.String(validate=validate.OneOf(
        ('number', 'select', 'text', 'radio', 'bool'),
    ), required=True)

    title = fields.String(required=False)
    default = fields.String(required=False)
    hint = fields.String(required=False)
    enabled = fields.Boolean(missing=True)
    precision = fields.Integer(required=False)
    range = fields.Tuple((fields.Integer(), fields.Integer()), required=False)
    choices = fields.Nested(Choice, many=True, required=False)
    multiple = fields.Boolean(required=False)


choices = ('divider', 'header', 'paragraph', 'info', 'setting', 'group')


class Item(Schema):
    type = fields.String(validate=validate.OneOf(choices))
    value = custom_fields.Typed(
        'type', {
            'group': fields.Nested(lambda: Item())
        },
        fields.String(),
        fields.String(validate=validate.OneOf(choices)),
        required=False
    )


class Settings(Schema):
    settings = fields.Nested(SettingItem, many=True, missing=list)
    items = fields.Nested(Item, many=True, missing=list)
