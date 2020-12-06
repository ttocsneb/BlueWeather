from marshmallow import Schema, fields

from . import custom_fields


class Choice(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(missing=True)


class Setting(Schema):
    name = fields.String(required=True)
    title = fields.String(required=False)
    hint = fields.String(required=False)
    enabled = fields.Boolean(missing=True)
    type = fields.String(required=True)


class Choices(Setting):
    choices = fields.Nested(Choice, required=True, many=True)
    many = fields.Boolean(missing=False)
    default = fields.String(required=False)


class Input(Setting):
    default = fields.String(required=False)


class Number(Setting):
    default = fields.Number(required=False)
    step = fields.Integer(required=False)
    range = fields.Tuple((fields.Number(), fields.Number()), required=False)


class DateTime(Setting):
    default = fields.DateTime(required=False)


class Time(Setting):
    default = fields.Time(required=False)


class Date(Setting):
    default = fields.Date(required=False)


class TimeDelta(Setting):
    default = fields.TimeDelta(required=False)


class Item(Schema):
    type = fields.String(required=True)
    value = fields.String(required=True)


class Divider(Schema):
    type = fields.String(required=True)


class Interface(Schema):
    settings = custom_fields.Combine([
        (('choices', 'select'), Choice),
        (('textarea', 'text', 'email', 'password', 'url'), Input),
        (('number', 'spin', 'range'), Number),
        ('datetime', DateTime),
        ('date', Date),
        ('time', Time),
        ('timedelta', TimeDelta)
    ], key="type", key_field=fields.String(required=True), many=True)
    items = custom_fields.Combine([
        ('divider', Divider),
        (('setting', 'header', 'paragraph', 'info'), Item)
    ], key="type", key_field=fields.String(required=True), many=True)
