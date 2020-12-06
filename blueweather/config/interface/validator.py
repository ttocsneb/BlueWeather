from marshmallow import Schema, fields, validate


choices = ('choices', 'select')
text = ('textarea', 'text', 'email', 'password', 'url')
number = ('number', 'spin', 'range')
datetime = ('datetime')
date = ('date')
time = ('time')
timedelta = ('timedelta')


def generate_field(setting: dict) -> fields.Field:
    """
    Generate a field item from a setting

    :param setting: setting

    :return: field for the setting
    """
    typ = setting['type']

    if typ in number:
        precision = setting.get('step')
        if precision == 0:
            return fields.Integer(missing=None)
        else:
            return fields.Float(missing=None)
        return fields.Number(missing=None)
    if typ in text:
        return fields.String(missing=None)
    if typ in choices:
        return fields.String(validate=validate.OneOf(
            list(map(lambda x: x['key'], setting.get('choices', [])))
        ), many=setting.get('many'))
    if typ in date:
        return fields.Date()
    if typ in datetime:
        return fields.DateTime()
    if typ in time:
        return fields.Time()
    if typ in timedelta:
        return fields.TimeDelta()


def generate_schema(interface: dict) -> Schema:
    """
    Generate a settings schema from an interface

    :param interface:

    :return: Schema for the interface settings
    """

    schema = dict(
        (setting['name'], generate_field(setting))
        for setting in interface['settings']
    )

    return Schema.from_dict(schema)(unknown='EXCLUDE')
