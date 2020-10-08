from .schema import Settings


def validate_interface(interface: dict):
    """
    Validate an interface.

    :param interface: interface to validate

    :return: validated interface

    :raises: marshmallow.ValidationError
    """
    schema = Settings()
    return schema.load(interface)
