"""
The DAO is the link between BlueWeather and the plugins.
"""
import markdown2
from stringlike.lazy import CachedLazyString
import inspect

from django.apps import AppConfig

from .manager import DriverManager

try:
    from importlib import metadata
except ImportError:
    print("warning: Could not import importlib")
    metadata = None


class PluginInfo:
    """
    Get info about a plugin
    """
    @classmethod
    def get_metadata(cls, app: AppConfig) -> dict:
        """
        Get the metadata for a plugin

        :param app: the app the plugin belongs to

        :return: metadata for the plugin

            .. code-block:: typescript

                interface Metadata {
                    packageName: string
                    version?: string
                    summary?: string
                    homepage?: string
                    author?: string
                    email?: string
                    license?: string
                    description?: html
                }

        """
        raw = metadata.metadata(app.name.split('.')[0])

        # The description can be either the payload of the message,
        # or a variable called description
        if hasattr(app, 'description'):
            raw_description = inspect.cleandoc(app.description)
        else:
            raw_description = inspect.cleandoc(raw.get('description', ''))
        if not raw_description:
            raw_description = raw.get_payload()

        if raw_description:
            description = CachedLazyString(lambda: markdown2.markdown(
                raw_description,
                extras=[
                    'tables',
                    'target-blank-lines',
                    'fenced-code-blocks',
                    'task_list'
                ]
            ))
        else:
            description = None

        def get(key: str, default: str = None):
            default = default or key
            if hasattr(app, default):
                return getattr(app, default)
            val = raw.get(key)
            if val == 'UNKNOWN':
                return None
            return val

        return {
            'packageName': get('name', 'packageName'),
            'label': app.label,
            'version': get('version'),
            'summary': get('summary'),
            'homepage': get('home-page', 'homepage'),
            'author': get('author'),
            'email': get('author-email', 'email'),
            'license': get('license'),
            'description': description
        }


class Weather:
    """
    Get the weather from the weather driver
    """

    @staticmethod
    def on_weather_request(man: DriverManager) -> dict:
        """
        request the weather from the weather driver

        :param plugin: driver

        :return: weather data
        """
        return next(man.mapCall("on_weather_request"))