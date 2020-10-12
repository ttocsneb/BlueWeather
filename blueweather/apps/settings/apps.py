from django.apps import AppConfig
from django.conf import settings

from . import config


class SettingsConfig(AppConfig):
    name = 'blueweather.apps.settings'
    label = 'settings'
    verbose_name = 'Settings'
    icon = 'fas fa-cog'
    route = 'settings:index'
    login_required = True

    api = 'blueweather.apps.settings.api'

    def ready(self):
        config.initialize()
        if settings.CONFIG.modified:
            settings.CONFIG.save()
