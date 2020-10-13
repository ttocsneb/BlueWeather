
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render

from blueweather import utils

from . import methods


@login_required
def index(request: HttpRequest):
    """
    The main page for managing plugins
    """
    return render(request, 'plugins/plugins.html', context={
        'name': 'Plugins'
    })


def plugin_list(request: HttpRequest):
    """

    :param page: page number
    :param size: items per page

    :return: plugin list

        .. code-block:: typescript

            interface Response {
                plugins: PluginList
                pages: number
                page: number
            }

        see :meth:`~blueweather.apps.plugins.methods.plugin_list` for
        :code:`PluginList`

    """
    try:
        page = int(request.GET.get('page', 0))
        size = int(request.GET.get('size', 10))
    except ValueError:
        return JsonResponse({
            'message': 'page and items should be numbers'
        }, status=400)

    pages = methods.pageify(methods.plugin_list(), size)

    page = max(0, min(page, len(pages) - 1))

    return JsonResponse({
        'plugins': pages[page],
        'pages': len(pages),
        'page': page
    }, encoder=utils.JsonEncoder)
