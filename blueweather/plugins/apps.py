from django.apps import AppConfig


class ExtensionsConfig(AppConfig):
    name = 'blueweather.plugins'
    label = 'blueweather.plugins'
    verbose_name = 'Plugins'
    icon = 'fas fa-puzzle-piece'
    route = 'plugins:index'
