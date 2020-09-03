import math

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render

from blueweather.apps.api.decorators import csrf_authorization_required


@login_required
def index(request: HttpRequest):
    """
    The main page for managing plugins
    """
    return render(request, 'plugins/plugins.html', context={
        'name': 'Plugins',
        'extensions': settings.EXTENSIONS.getPluginList()
    })


@csrf_authorization_required
@require_POST
def plugin_list(request: HttpRequest):
    """
    Get a list of all the plugins as a json list.

    .. note::

        The shown parameters are GET parameters

    :param page: page number (default: 0)
    :param items: number of items per page (default: 10)

    :return:

        .. code-block:: json

            {
                "plugins": {
                    "plugin-name": {}
                },
                "page": "page-number",
                "items": "plugins-per-page",
                "pages": "total-pages",
                "total": "total-plugins"
            }

        See :meth:`~blueweather.plugins.ExtensionsSingleton.getPluginList` for
        plugin object description.
    """
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
