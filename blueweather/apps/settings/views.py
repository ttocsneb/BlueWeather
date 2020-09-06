from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render
from blueweather.apps.api.decorators import csrf_authorization_required


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