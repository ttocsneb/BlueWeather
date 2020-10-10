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

# TODO Load all the api extensions
