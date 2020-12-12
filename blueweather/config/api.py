"""
ReST API for accessing the settings

Config api prefix: :code:`/api/config/`
"""
from marshmallow import ValidationError

from django.http.request import HttpRequest

from dresta.decorators import api
from dresta.exceptions import APIError, NotFoundError, ValidateError

from . import methods


@api()
def interfaces(request: HttpRequest):
    """
    Get the settings interface

    :method: any
    """
    return methods.get_settings_interfaces()


@api(name="get")
def get_settings(request: HttpRequest, label: str):
    """
    Get the current settings

    :method: any

    :name: get

    :param str label: plugin label
    """

    try:
        return methods.get_settings(label)
    except LookupError:
        raise NotFoundError(detail="Could not find label")
    except ValidationError as error:
        raise ValidateError.fromMarshmallowError(error)
    except Exception:
        raise APIError(500, detail="App improperly configured")


@api(name="set", methods=['POST'])
def set_settings(request: HttpRequest, label: str, settings: dict):
    """
    Set the Settings

    :method: POST

    :name: set

    :param str label: plugin label
    :param dict settings: settings
    """
    setting = None
    try:
        for k, v in settings.items():
            setting = k
            methods.set_setting(label, k, v)
        return methods.get_settings(label)
    except KeyError:
        methods.revert_settings()
        raise ValidateError(
            {setting: ['Not a valid setting']},
            detail="Setting does not exist"
        )
    except LookupError:
        methods.revert_settings()
        raise NotFoundError(detail="Could not find label")
    except ValidationError as error:
        methods.revert_settings()
        raise ValidateError.fromMarshmallowError(error)
    except Exception:
        methods.revert_settings()
        raise APIError(500, detail="App improperly configured")


@api()
def load(request: HttpRequest):
    """
    Load the settings from disk

    :method: any
    """
    methods.revert_settings()


@api()
def apply(request: HttpRequest):
    """
    Apply the settings to disk

    :method: any
    """
    methods.apply_settings()
