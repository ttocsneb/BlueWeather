from django.apps import AppConfig
from django.conf import settings

from . import methods


class SettingsConfig(AppConfig):
    name = 'blueweather.config'
    label = 'settings'
    verbose_name = 'Settings'
    icon = 'fas fa-cog'
    route = 'settings:index'
    login_required = True

    def ready(self):
        ready_settings = methods.initialize()
        if settings.CONFIG.modified:
            settings.CONFIG.save()

        for conf in ready_settings:
            conf.plugin.ready()
