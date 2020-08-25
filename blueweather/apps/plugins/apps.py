from django.apps import AppConfig
from django.conf import settings

from blueweather.plugins import dao

import logging


class ExtensionsConfig(AppConfig):
    name = 'blueweather.apps.plugins'
    label = 'blueweather.apps.plugins'
    verbose_name = 'Plugins'
    icon = 'fas fa-puzzle-piece'
    route = 'plugins:index'
    login_required = True

    def ready(self):
        logger = logging.getLogger(__name__)
        logger.info("Server is now ready")
        dao.Startup.on_startup(settings.EXTENSIONS.startup)
