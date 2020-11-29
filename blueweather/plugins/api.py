from django.http.request import HttpRequest
from django.conf import settings

from blueweather.api.decorators import api
from blueweather.api.utils import pagify

from . import utils, tools


@api()
def info(request: HttpRequest, page: int = 0, size: int = 10):
    """
    Get the info of all the enabled plugins
    """
    plugin_infos = []

    for enabled in settings.CONFIG.plugins.enabled:
        try:
            app = utils.get_app(enabled)
            plugin_infos.append(tools.PluginInfo.get_metadata(app))
        except LookupError:
            pass

    return pagify(plugin_infos, page, size, 'info')
