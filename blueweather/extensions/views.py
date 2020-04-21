from django.shortcuts import render
from django.http.response import JsonResponse
from django.conf import settings

from blueweather.plugins import map as plugin_map


def index(request):
    return render(request, 'extensions/extensions.html', context={
        'name': 'Extensions',
        'extensions': settings.EXTENSIONS.getPluginList()
    })


def plugin_list(request):
    return JsonResponse(settings.EXTENSIONS.getPluginList())
