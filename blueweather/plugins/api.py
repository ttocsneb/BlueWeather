"""
Access the Plugin data from the ReST API.

Plugins api prefix: :code:`/api/plugins/`
"""
from django.http.request import HttpRequest
from django.conf import settings

from dresta.decorators import api
from dresta.utils import pagify

from . import utils, tools


@api()
def info(request: HttpRequest, page: int = 0, size: int = 10):
    """
    Get the info of all the enabled plugins

    :method: any

    :param int page: page number
    :param int size: size of pages
    """
    plugin_infos = []

    for enabled in settings.CONFIG.plugins.enabled:
        try:
            app = utils.get_app(enabled)
            plugin_infos.append(tools.PluginInfo.get_metadata(app))
        except LookupError:
            pass

    return pagify(plugin_infos, page, size, 'info')
