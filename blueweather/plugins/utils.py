import importlib
import inspect

from django.apps import AppConfig

from typing import List, Tuple


def load_app_module(app: AppConfig, module: str):
    """
    Load a module that belongs to an app

    :param app: app to import from
    :param module: module name

    :return: found module or None
    """
    relative = '.%s' % module
    try:
        return importlib.import_module(relative, package=app.name)
    except ImportError:
        return None


def find_members(module) -> List[Tuple[str, object]]:
    """
    Find all the members of a module

    :param module: module

    :return: all public members of the module
    """
    return [
        m for m in inspect.getmembers(module)
        if not m[0].startswith('__')
    ]
