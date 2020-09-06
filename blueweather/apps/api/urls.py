from django.urls import include, path
from django.conf import settings

from blueweather.plugins import dao
from blueweather.apps.plugins import urls as plugin_urls
from blueweather.apps.settings import urls as settings_urls

urlpatterns = [
    path('plugins/', include(
        (plugin_urls.get_api_urlpatterns(), 'plugins'),
        namespace='plugins'
    )),
    path('settings/', include(
        (settings_urls.get_api_urlpatterns(), 'settings'),
        namespace='settings'
    ))
]

# Load all the api extensions
if settings.EXTENSIONS.api.extensions:
    for name, patterns in settings.EXTENSIONS.api.map(
            dao.API.get_api_urlpatterns):
        urlpatterns.append(
            path('%s/' % name, include(
                (patterns, name), namespace=name
            ))
        )
