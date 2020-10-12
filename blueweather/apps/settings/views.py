import logging
from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_POST

from marshmallow import ValidationError

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
    """
    interface = config.get_settings_interface()
    return JsonResponse(interface)


def get_settings(request: HttpRequest, app: str):
    """
    Get the current settings

    :param app: app to get the settings from
    """

    app = app.replace('-', '.')

    try:
        return JsonResponse(config.get_settings(app))
    except LookupError:
        raise Http404
    except ValidationError as validation:
        logging.getLogger(__name__).exception(
            'Could not validate settings'
        )
        return JsonResponse({
            'message': 'settings improperly configured',
            'validation': validation.messages
        }, status=500)
    except Exception:
        logging.getLogger(__name__).exception(
            'An exception occurred while getting the settings'
        )
        return JsonResponse({
            'message': 'app improperly configured'
        }, status=500)


@require_POST
def set_settings(request: HttpRequest, app: str):
    """
    Apply the settings

    :param app: app to set the settings to
    :param setting: name of the setting to change
    :param value: value of the new setting
    """

    app = app.replace('-', '.')
    setting = request.POST.get('setting')
    value = request.POST.get('value')

    if setting is None or value is None:
        return JsonResponse({
            'message': 'setting and app parameters are required'
        }, status=400)

    try:
        config.set_setting(app, setting, value)
        return JsonResponse(
            config.get_settings(app)
        )
    except KeyError:
        return JsonResponse({
            'message': 'setting does not exist'
        })
    except LookupError:
        return JsonResponse({
            'message': 'app does not exist'
        }, status=400)
    except ValidationError as error:
        return JsonResponse({
            'message': error.messages
        }, status=400)
    except Exception:
        logging.getLogger(__name__).exception(
            'An exception occurred while setting a setting'
        )
        return JsonResponse({
            'message': 'app improperly configured'
        }, status=500)


def revert_settings(request: HttpRequest):
    """
    Revert the changes to what's stored on disk
    """

    config.revert_settings()

    return HttpResponse('')


def apply_settings(request: HttpRequest):
    """
    Apply the changes made to disk
    """

    config.apply_settings()

    return HttpResponse('')
