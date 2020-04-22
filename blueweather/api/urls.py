from django.urls import include, path
from django.conf import settings
from blueweather.plugins import map as plugin_map, urls

urlpatterns = [
    path('plugins/', include(
        (urls.get_api_urlpatterns(), 'plugins'),
        namespace='plugins'
    ))
]

# Load all the api extensions
if settings.EXTENSIONS.api.extensions:
    for name, patterns in settings.EXTENSIONS.api.map(
            plugin_map.API.get_api_urlpatterns):
        urlpatterns.append(
            path('%s/' % name, include(
                (patterns, name), namespace=name
            ))
        )
