"""blueweather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .plugins import dao

handler404 = 'blueweather.views.pageNotFound'
handler403 = 'blueweather.views.forbidden'
handler400 = 'blueweather.views.badRequest'
handler500 = 'blueweather.views.internalServerError'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('blueweather.apps.accounts.urls')),
    path('', include(
        ('blueweather.apps.weather.urls', 'weather'),
        namespace='weather'
    )),
    path('plugins/', include(
        ('blueweather.apps.plugins.urls', 'plugins'),
        namespace='plugins'
    )),
    path('api/', include(
        ('blueweather.apps.api.urls', 'api'),
        namespace='api'
    ))
]

# Add plugin urls
for ext in settings.EXTENSIONS.djangoApp:
    _, url, name = dao.DjangoApp.get_url_info(ext)
    _, path = dao.DjangoApp.get_app_name(ext)
    urlpatterns.append(path(url, include((path, name), name)))
