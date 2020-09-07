from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from blueweather.apps.api.decorators import csrf_authorization_required
from urllib.parse import unquote

@login_required
def index(request: HttpRequest):
    """
    The main page for the settings
    """

    conf = settings.CONFIG.dump()

    def getSetting(key: str=None) -> str:
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

    :param settings:

        .. code-block:: json

            {
                "settings": {
                    "name-of-setting": "value"
                }
            }
    
    :return:

        .. code-block:: json

            {
                "success": "true or false",
                "reason": "Reason why unsuccessful"
            }
    """
    new_settings = json.loads(request.body).get('settings')

    print("post: %s" % new_settings)
    return JsonResponse({"success": True})
