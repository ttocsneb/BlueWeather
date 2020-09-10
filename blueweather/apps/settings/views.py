import logging
from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from blueweather.apps.api.decorators import csrf_authorization_required


@login_required
def index(request: HttpRequest):
    """
    The main page for the settings
    """

    conf = settings.CONFIG.dump()

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
        'settings': getSetting
    })


@csrf_authorization_required
@require_POST
def set_settings(request: HttpRequest):
    """
    Set a value of the settings

    :type POST:

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

        .. code-block:: json

            {
                "success": "true or false",
                "reason": "Reason why unsuccessful"
            }
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

    # Load the data
    try:
        data = json.loads(request.body)
        new_settings = data.get('settings')
        namespace = data.get('namespace', '').split('.')
    except json.decoder.JSONDecodeError as e:
        logger.exception("Could not parse Settings")
        return JsonResponse({"success": False, "reason": str(e)})

    # Parse the settings into a settings object
    for k, v in new_settings.items():
        keys = [i for i in namespace + k.split('.') if i]
        load_settings(config, keys, v)

    # TODO merge the new settings with the existing settings

    return JsonResponse({"success": True})
