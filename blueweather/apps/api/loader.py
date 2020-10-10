import logging
from django.apps import registry
from django.urls import path, include

from typing import List


def get_url_patterns() -> List[path]:
    """
    Get all the url patterns for each app that uses them

    .. note::

        The patterns are loaded in from the AppConfig with the setting

        .. code-block:: python

            api = 'path.to.api'

        In the api module, there should be the variable: :code:`urlpatterns`
        just like in the urls module.

        Each pattern gets the namespace of :code:`api:app_label`

    :return: list of urlpatterns
    """

    logger = logging.getLogger(__name__)
    patterns = []

    for config in registry.apps.get_app_configs():
        if hasattr(config, 'api'):
            patterns.append(
                path(
                    '{}/'.format(config.label),
                    include((config.api, config.name), config.label)
                )
            )
            logger.info(
                "Loaded api url patterns for '%s'", config.name
            )

    return patterns
