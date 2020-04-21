from django.apps import AppConfig


class ExtensionsConfig(AppConfig):
    name = 'blueweather.extensions'
    label = 'blueweather.extensions'
    verbose_name = 'Extensions'
    icon = 'fas fa-puzzle-piece'
    route = 'extensions:extensions'
