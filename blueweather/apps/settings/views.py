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

from . import config


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


def get_settings_interface(request: HttpRequest):
    """
    Get the settings interface

    :param app: app to get the settings from
    """

    app = request.GET.get('app')

    interface = config.get_settings_interface(app)

    # TODO Return the settings interface


def get_settings(request: HttpRequest):
    """
    Get the current settings

    :param app: app to get the settings from
    """

    app = request.GET.get('app')

    settings = config.get_settings(app)

    # TODO Return the App Config


def set_settings(request: HttpRequest):
    """
    Apply the settings

    :param app: app to set the settings to
    :param setting: name of the setting to change
    :param value: value of the new setting
    """

    app = request.POST.get('app')
    setting = request.POST.get('setting')
    value = request.POST.get('value')

    # TODO Find the App config in the config obj
    # TODO Apply the setting to the config


def revert_settings(request: HttpRequest):
    """
    Revert the changes to what's stored on disk
    """

    # TODO read the settings from disk, replacing the settings in memory


def apply_settings(request: HttpRequest):
    """
    Apply the changes made to disk
    """

    # TODO Save the settings to disk
