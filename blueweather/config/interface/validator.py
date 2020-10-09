from marshmallow import Schema, fields


def generate_field(setting: dict) -> fields.Field:
    """
    Generate a field item from a setting

    :param setting: setting

    :return: field for the setting
    """
    typ = setting['type']
    if typ == 'number':
        precision = setting['options'].get('precision')
        if precision == 0:
            return fields.Integer(missing=None)
        else:
            return fields.Float(missing=None)
        return fields.Number(missing=None)
    if typ in ['select', 'text', 'radio']:
        return fields.String(missing=None)
    if typ == 'bool':
        return fields.Boolean(missing=None)


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
