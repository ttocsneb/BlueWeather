from django.shortcuts import render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.conf import settings
import math


def index(request):
    return render(request, 'plugins/plugins.html', context={
        'name': 'Plugins',
        'extensions': settings.EXTENSIONS.getPluginList()
    })


def plugin_list(request: HttpRequest):
    plugins_raw = settings.EXTENSIONS.getPluginList()

    page = int(request.GET.get('page', 0))
    items = int(request.GET.get('items', 10))
    pages = math.ceil(len(plugins_raw) / items)
    page = max(min(page, pages - 1), 0)

    start = page * items
    end = start + items

    plugin_names = sorted(list(plugins_raw.keys()))[start:end]

    plugins = dict()
    plugins['plugins'] = dict([(k, plugins_raw[k]) for k in plugin_names])
    plugins['page'] = page
    plugins['items'] = items
    plugins['pages'] = pages
    plugins['total'] = len(plugins_raw)
    return JsonResponse(plugins)
