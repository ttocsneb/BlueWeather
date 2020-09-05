from django.apps import AppConfig


class SettingsConfig(AppConfig):
    name = 'blueweather.apps.settings'
    label = 'blueweather.apps.settings'
    verbose_name = 'Settings'
    icon = 'fas fa-cog'
    route = 'settings:index'
    login_required = True