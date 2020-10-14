import logging
from django.shortcuts import render
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_POST

from django.apps import registry, AppConfig

from marshmallow import ValidationError

from . import methods


@login_required
def index(request: HttpRequest):
    """
    The main page for the settings
    """

    interfaces = methods.get_settings_interfaces()

    app_names = dict(
        (app.label, app.verbose_name)
        for app in registry.apps.get_app_configs()
        if hasattr(app, 'verbose_name')
    )

    return render(request, 'settings/settings.html.j2', context={
        'name': 'Settings',
        'interfaces': interfaces,
        'modified': json.dumps(settings.CONFIG.modified),
        'get_settings': methods.get_settings,
        'verbose_names': app_names
    })


def get_settings_interfaces(request: HttpRequest):
    """
    Get the settings interface
    """
    return JsonResponse(methods.get_settings_interfaces())


def get_settings(request: HttpRequest, app: str):
    """
    Get the current settings

    :param app: app to get the settings from
    """

    app = app.replace('-', '.')

    try:
        return JsonResponse(methods.get_settings(app))
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
        methods.set_setting(app, setting, value)
        return JsonResponse(
            methods.get_settings(app)
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

    methods.revert_settings()

    return HttpResponse('')


def apply_settings(request: HttpRequest):
    """
    Apply the changes made to disk
    """

    methods.apply_settings()

    return HttpResponse('')
