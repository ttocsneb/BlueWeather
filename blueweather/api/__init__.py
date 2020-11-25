"""
Manages all api views and their routes

To get started, create an :code:`api.py` file in your app folder:

.. code-block:: python

    from blueweather.api.decorators import api

    @api()
    def myView(request: HttpRequest, arg1: int, arg2: int):
        # TODO: process request
        return {
            "success": True
        }

Then in your :code:`AppConfig` object located in :code:`apps.py`, add the
:code:`api` attribute to show where the api view is.

.. code-block:: python

    class MyAppConfig(AppConfig):
        name = 'myapp'
        label = 'myapp'

        api = 'myapp.api'

"""
import inspect

from importlib import import_module

from django.urls import path, include
from django.apps import apps

from typing import List, Tuple


def include_api_patterns(module: str):
    """
    Load the api views in a module into a urlpattern

    This will load all api views from the module. For an object to be
    considered an api view it must have a urlpattern property.

    .. note::

        The recommended way to make your api views is by using the
        :meth:`blueweather.api.decorators.api` decorator.

    :param module: module path

    :return: the included api patterns
    """
    module = import_module(module)
    # Get all members, ignore private members
    members = [
        i for i in inspect.getmembers(module)
        if not i[0].startswith('__')
    ]
    # Get all members that have the 'urlpattern' attr (it is an api view)
    views = [
        member
        for member in members
        if hasattr(member, 'urlpattern')
    ]

    # Include all the views
    return include([
        view.urlpattern
        for view in views
    ])


def include_all_api_patterns():
    """
    Load all of the api patterns from every app

    To mark that your app has api patterns, set the :code:`api` attribute
    of your :code:`AppConfig` object to the full path of your api views module

    .. code-block:: python

        class MyAppConfig(AppConfig):
            name = 'myapp'
            label = 'myapp'

            api = 'myapp.api'

    :return: the included api patterns
    """
    all_modules: List[Tuple[str, str]] = []

    # Get all the apps that are configured for the api
    for config in apps.get_app_configs():
        if hasattr(config, 'api'):
            all_modules.append(
                (config.label, config.api)
            )

    # Load all the api patterns
    all_patterns = [
        path('%s/' % name, include_api_patterns(module))
        for name, module in all_modules
    ]

    return include(all_patterns)
