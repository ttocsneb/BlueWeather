"""
The DAO is the link between BlueWeather and the plugins.
"""
from stevedore.extension import Extension, ExtensionManager
from stevedore.dispatch import DispatchExtensionManager
from stevedore.exception import NoMatches

import re
import markdown2

try:
    from importlib import metadata
except ImportError:
    print("warning: Could not import importlib")
    metadata = None

from typing import List, Dict, Set, Tuple

prettyNames = {
    'blueweather.plugins.weather': "Weather",
    'blueweather.plugins.unitconv': "Unit-Conversion",
    'blueweather.plugins.app': "App"
}
'''Pretty Names for each Plugin Type'''
builtins = [
    'imperialConverter',
    'metricConverter',
    'dummyWeather'
]
'''Built-in plugins'''


class PluginInfo:
    """
    Get info about a plugin
    """
    @classmethod
    def get_metadata(cls, ext: Extension) -> dict:
        """
        Get the metadata for a plugin

        :param ext: any extension that belongs to the plugin

        :return: metadata for the plugin

            .. code-block:: typescript

                interface Metadata {
                    name: string
                    version?: string
                    summary?: string
                    homepage?: string
                    author?: string
                    email?: string
                    license?: string
                    description?: html
                }

        """
        raw = metadata.metadata(ext.entry_point_target.split('.')[0])

        def fix_tabs(text: str) -> str:
            """
            When 'description' is used, newlines get 8 spaces of tabs, which
            mess up markdown parsing

            :param text: text to fix

            :return: fixed tabs
            """
            fixed = re.sub(r"^ {8}", '', text, flags=re.MULTILINE)
            print(fixed)
            return fixed

        # The description can be either the payload of the message,
        # or a variable called description
        raw_description = fix_tabs(raw.get('description', ''))
        if not raw_description:
            raw_description = raw.get_payload()

        if raw_description:
            description = markdown2.markdown(
                raw_description,
                extras=[
                    'tables',
                    'target-blank-lines',
                    'fenced-code-blocks',
                    'task_list'
                ]
            )
        else:
            description = None

        def get(key: str, default: str = None):
            val = raw.get(key, default)
            if val == 'UNKNOWN':
                return None
            return val

        return {
            'name': get('name', ext.name),
            'version': get('version'),
            'summary': get('summary'),
            'homepage': get('home-page'),
            'author': get('author'),
            'email': get('author-email'),
            'license': get('license'),
            'description': description
        }


class App:
    """
    Get the app name for the plugin
    """

    @staticmethod
    def get_app_names(man: ExtensionManager) -> List[str]:
        """
        Get all the app names for the extensions

        :param man: app extension manager

        :return: list of app names
        """

        def get_app_name(ext: Extension, *args, **kwds):
            return ext.obj.app_name

        try:
            return man.map(get_app_name)
        except NoMatches:
            return []


class Weather:
    """
    Get the weather from the weather driver
    """

    @staticmethod
    def on_weather_request(ext: Extension) -> dict:
        """
        request the weather from the weather driver

        :param ext: driver

        :return: weather data
        """
        return ext.obj.on_weather_request()


class UnitConversion:
    """
    Convert diffent units of measurement
    """

    @staticmethod
    def conversions(man: DispatchExtensionManager) -> Dict[str, Set[str]]:
        """
        Get all the basic conversions

        :param man: UnitConversion Extension Manager

        :return: Possible Conversions
        """
        units = dict()
        for name, conversions in man.map(
                lambda *args, **kwargs: True,  # Something seems fishy
                UnitConversion.get_conversion_types):
            if conversions is None:
                continue
            for from_type, to_type in conversions:
                if from_type not in units:
                    units[from_type] = set()
                units[from_type].add(to_type)
        return units

    @staticmethod
    def all_conversions(man: DispatchExtensionManager = None,
                        units: Dict[str, Set[str]] = None
                        ) -> Dict[str, Set[str]]:
        """
        Get all the possible conversions

        This finds all the possible conversions by using recursive conversions

        :param man: UnitConversion Extension Manager
        :param units: All the basic conversions

        :return: All the possible conversions
        """
        if units is None:
            units = UnitConversion.conversions(man)
        # Add secondary conversions (Conversions that can be made by
        # converting a conversion)
        for k, v in units.items():
            for u in v:
                if u in units:
                    v.union(units[u])
        return units

    @staticmethod
    def convert(man: DispatchExtensionManager, data: float, from_type: str,
                to_type: str) -> Tuple[List[str], float]:
        """
        Convert from one type to another

        :param man: UnitConversion Extension Manager
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: name(s) of the extensions that performed the conversion, and
            the converted value
        """
        units = UnitConversion.conversions(man)

        if from_type not in units:
            raise KeyError("%s can not be converted to another type" %
                           from_type)
        to_types = units[from_type]

        def conv(d, from_t, to_t) -> (str, float):
            for ext in man.extensions:
                if not UnitConversion.on_request_conversion_check(
                        ext, d, from_t, to_t):
                    continue
                val = ext.obj.request_conversion(d, from_t, to_t)
                if val is not None:
                    return ext.name, val
            raise KeyError("%s can not be converted to %s" % (from_t, to_t))

        # It is a simple conversion, so we can convert directly
        if to_type in to_types:
            return conv(data, from_type, to_type)

        # It may be a complex (two part conversion) so we will need to see if
        # it is possible to convert

        from_types = set()
        for k, v in units.items():
            if to_type in v:
                from_types.add(k)

        mid_type = None
        for t in units[from_type]:
            if t not in from_types:
                continue
            # Make the Middle conversion
            mid_type = t
            name1, data = conv(data, from_type, mid_type)

        if mid_type is None:
            raise KeyError("%s can not be converted to %s" %
                           (from_type, to_type))
        # Make final conversion
        name2, data = conv(data, mid_type, to_type)
        return (name1, name2), data

    @staticmethod
    def get_conversion_types(ext: Extension
                             ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Get the types that an extension can convert

        :param ext: extension

        :return: extension name, and possible conversions
        """
        return ext.name, ext.obj.get_conversion_types()

    @staticmethod
    def on_request_conversion_check(ext: Extension, data: float,
                                    from_type: str, to_type: str) -> bool:
        """
        Check if a conversion can be performed

        :param ext: extension
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: True if the conversion is possible
        """
        _, types = UnitConversion.get_conversion_types(ext)
        return next(
            (True for t in types if t[0] == from_type and t[1] == to_type),
            False
        )

    @staticmethod
    def request_conversion(ext: Extension, data: float, from_type: str,
                           to_type: str) -> (str, float):
        """
        Request a conversion to be made

        :param ext: extension
        :param data: value to convert from
        :param from_type: type to convert from
        :param to_type: type to convert to

        :return: the name of the extension, and the converted value
        """
        data = ext.obj.request_conversion(data, from_type, to_type)
        if data is not None:
            return ext.name, data
