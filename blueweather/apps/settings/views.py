import logging
from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from blueweather.apps.api.decorators import csrf_authorization_required
from marshmallow.exceptions import MarshmallowError, ValidationError


@login_required
def index(request: HttpRequest):
    """
    The main page for the settings
    """

    conf = settings.CONFIG.serialize()

    def getSetting(key: str = None) -> str:
        if key is None:
            return json.dumps(conf)
        keys = key.split('.')
        setting = conf
        for k in keys:
            setting = setting[k]
        return json.dumps(setting)

    return render(request, 'settings/settings.html.j2', context={
        'name': 'Settings',
        'settings': getSetting,
        'modified': json.dumps(settings.CONFIG.modified)
    })


@csrf_authorization_required
@require_POST
def set_settings(request: HttpRequest):
    """
    Set a value of the settings

    :type: POST

    :param namespace: The starting point of each setting

        .. note::

            Each value can be any type of object

    :param settings: A dictionary of settings, and their values

    .. code-block:: json

        {
            "namespace": "starting.point",
            "settings": {
                "name.of.setting": "value"
            }
        }

    :return:

        * **success** - whether successful
        * **reason** - A human readable error why it was unsuccessful.
        * **validation** - An object describing which parameters were invalid.
        * **namespace** - The namespace from the request
        * **settings** - The current settings based on the given settings

        .. code-block:: json

            {
                "success": "true or false",
                "reason": "Reason why unsuccessful",
                "validation": {
                    "key": ["Reason why it's invalid"]
                },
                "namespace": "given.namespace"
                "settings": {
                    "key": "saved settings"
                }
            }

        .. note::

            **reason** and **validation** are only supplied if **success**
            is :code:`false`.
    """

    config = dict()

    logger = logging.getLogger(__name__)

    def load_settings(obj: dict, keys: list, value):
        if len(keys) == 1:
            obj[keys[0]] = value
        else:
            if keys[0] not in obj:
                obj[keys[0]] = dict()
            load_settings(obj[keys[0]], keys[1:], value)

    def apply_settings() -> dict:
        dest = dict()
        current = settings.CONFIG.serialize()

        def unload_settings(k: str, source: dict, keys: list,
                            destination: dict):
            if len(keys) == 1:
                destination[k] = source[keys[0]]
            else:
                unload_settings(k, source[keys[0]], keys[1:], destination)

        # Unload the setings into the response
        for k, v in new_settings.items():
            keys = [i for i in namespace + k.split('.') if i]
            unload_settings(k, current, keys, dest)

        return dest

    # Load the data
    try:
        data = json.loads(request.body)
        new_settings = data.get('settings')
        namespace = data.get('namespace', '').split('.')
    except json.decoder.JSONDecodeError as e:
        logger.exception("Could not parse Settings")
        return JsonResponse({
            "success": False,
            "reason": str(e),
            "namespace": namespace,
            "settings": apply_settings()
        })

    # Parse the settings into a settings object
    for k, v in new_settings.items():
        keys = [i for i in namespace + k.split('.') if i]
        load_settings(config, keys, v)

    # Merge the new settings with the existing settings

    conf = settings.CONFIG.serialize()

    def merge(orig: dict, new: dict):
        for k, v in new.items():
            if k in orig and isinstance(v, dict) and isinstance(orig[k], dict):
                merge(orig[k], v)
            else:
                orig[k] = v

    merge(conf, config)

    try:
        settings.CONFIG.deserialize(conf)
        settings.CONFIG.modified = True
    except ValidationError as e:
        logger.exception("The settings could not be deserialized")
        return JsonResponse({
            "success": False,
            "reason": "Invalid Settings",
            "validation": e.messages,
            "namespace": namespace,
            "settings": apply_settings()
        })
    except MarshmallowError as e:
        logger.exception("An error occurred while deserializing the settings")
        logger.error("Exception: %s", e)

        return JsonResponse({
            "success": False,
            "reason": str(e),
            "namespace": namespace,
            "settings": apply_settings()
        })

    # Return the updated settings

    return JsonResponse({
        "success": True,
        "namespace": namespace,
        "settings": apply_settings()
    })


@csrf_authorization_required
@require_POST
def save_settings(request: HttpRequest):
    """
    Save the loaded settings

    :type: POST
    """

    settings.CONFIG.save()


@csrf_authorization_required
@require_POST
def revert_settings(request: HttpRequest):
    """
    Revert the settings to what is stored on disk

    :type: POST
    """

    settings.CONFIG.load()