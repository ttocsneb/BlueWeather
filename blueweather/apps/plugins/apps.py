from django.apps import AppConfig


class ExtensionsConfig(AppConfig):
    name = 'blueweather.apps.plugins'
    label = 'blueweather.apps.plugins'
    verbose_name = 'Plugins'
    icon = 'fas fa-puzzle-piece'
    route = 'plugins:index'
    login_required = True
