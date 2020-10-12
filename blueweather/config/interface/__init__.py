from .schema import Settings
from . import validator

from typing import Union, Any


def validate_interface(interface: Union[dict, list]):
    """
    Validate an interface.

    :param interface: interface to validate

    :return: validated interface

    :raises: marshmallow.ValidationError
    """
    if isinstance(interface, list):
        schema = Settings(many=True)
        return schema.load(interface)
    schema = Settings()
    return schema.load(interface)


def read_settings(interface: dict, settings: dict) -> dict:
    """
    Read the settings, and only return the settings mentioned in the interface

    :param interface: pre-validated interface to use
    :param settings: settings to read

    :return: settings only containing interface
    """

    schema = validator.generate_schema(interface)
    return schema.load(settings)


def validate_setting(interface: dict, name: str, value) -> Any:
    """
    Validate a setting for an interface

    :param interface: pre-validated interface to use
    :param name: name of the setting
    :param value: value of the setting

    :return: validated setting

    :raise KeyError: if the setting doesn't exist
    :raise marshmallow.ValidationError: if the value isn't valid
    """

    try:
        setting = next(
            i for i in interface['settings']
            if i['name'] == name
        )
    except StopIteration as stop:
        raise KeyError from stop

    field = validator.generate_field(setting)
    return field.deserialize(value, name, {name: value})
