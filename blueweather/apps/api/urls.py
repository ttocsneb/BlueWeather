from django.urls import include, path
from django.conf import settings

from blueweather.plugins import dao
from blueweather.apps.plugins import urls

urlpatterns = [
    path('plugins/', include(
        (urls.get_api_urlpatterns(), 'plugins'),
        namespace='plugins'
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
