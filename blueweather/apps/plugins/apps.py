from django.apps import AppConfig
from django.conf import settings

from blueweather.plugins import dao

import logging


class ExtensionsConfig(AppConfig):
    name = 'blueweather.apps.plugins'
    label = 'plugins'
    verbose_name = 'Plugins'
    icon = 'fas fa-puzzle-piece'
    route = 'plugins:index'
    login_required = True

    api = 'blueweather.apps.plugins.api'

    def ready(self):
        settings.EXTENSIONS.invoke_all()
