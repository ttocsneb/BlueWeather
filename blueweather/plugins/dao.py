from marshmallow import Schema
from stevedore.extension import Extension, ExtensionManager
from stevedore.dispatch import DispatchExtensionManager

prettyNames = {
    "blueweather.plugins.plugin": "Plugin-Info",
    "blueweather.plugins.weather": "Weather",
    'blueweather.plugins.django': "Web-App",
    'blueweather.plugins.startup': "Startup",
    'blueweather.plugins.settings': "Settings",
    'blueweather.plugins.unitconv': "Unit-Conversion",
    'blueweather.plugins.api': "ReST-API"
}
builtins = [
    'imperialConverter',
    'metricConverter',
    'dummyWeather'
]


def strip_name(tup: tuple):
    return map(lambda x: x[1], tup)


class Plugin:
    @staticmethod
    def get_plugin_name(ext: Extension) -> str:
        return ext.obj.get_plugin_name()

    @staticmethod
    def get_plugin_description(ext: Extension) -> str:
        return ext.obj.get_plugin_description()

    @staticmethod
    def get_plugin_author(ext: Extension) -> str:
        return ext.obj.get_plugin_author()

    @staticmethod
    def get_plugin_url(ext: Extension) -> str:
        return ext.obj.get_plugin_url()


class Startup:
    @staticmethod
    def on_startup(ext: Extension, host: str, port: int):
        ext.obj.on_startup(host, port)

    @staticmethod
    def on_after_startup(ext: Extension):
        ext.obj.on_after_startup()

    @staticmethod
    def on_shutdown(ext: Extension):
        ext.obj.on_shutdown()


class DjangoApp:
    @staticmethod
    def getApps(man: ExtensionManager) -> list:
        apps = list()
        for ext in man.extensions:
            apps.append(DjangoApp.get_app_name(ext)[1])
        return apps

    @staticmethod
    def get_app_name(ext: Extension) -> (str, str):
        return ext.name, ext.obj.get_app_name()

    @staticmethod
    def get_url_info(ext: Extension) -> (str, str, str):
        data = ext.obj.get_url_info()
        if isinstance(data, tuple):
            return ext.name, data[0], data[1]
        return ext.name, data, data.replace('/', '.')


class API:
    @staticmethod
    def allApiPatterns(man: ExtensionManager) -> list:
        patterns = list()
        for ext in man.extensions:
            patterns.extend(API.get_api_urlpatterns(ext)[1])
        return patterns

    @staticmethod
    def get_api_urlpatterns(ext: Extension) -> (str, list):
        return ext.name, ext.obj.get_api_urlpatterns()


class Settings:
    @staticmethod
    def get_default_settings(ext: Extension) -> (str, dict):
        return ext.name, ext.obj.get_default_settings()

    @staticmethod
    def get_required_settings(ext: Extension) -> (str, dict):
        return ext.name, ext.obj.get_required_settings()

    @staticmethod
    def get_settings_schema(ext: Extension) -> (str, Schema):
        return ext.name, ext.obj.get_settings_schema()

    @staticmethod
    def on_settings_migrate(ext: Extension, version: int, settings: dict
                            ) -> (str, dict):
        return ext.name, ext.obj.on_settings_migrate(version, settings)

    @staticmethod
    def on_settings_initialized(ext: Extension):
        ext.obj.on_settings_initialized()


class Weather:
    @staticmethod
    def on_weather_request(ext: Extension) -> (str, dict):
        return ext.name, ext.obj.on_weather_request()


class UnitConversion:
    @staticmethod
    def conversions(man: DispatchExtensionManager) -> dict:
        units = dict()
        for name, conversions in man.map(lambda *args, **kwargs: True,
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
                        units: dict = None) -> dict:
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
                to_type: str) -> (str, float):
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
                val = ext.obj.on_request_conversion(d, from_t, to_t)
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
    def get_conversion_types(ext: Extension) -> (str, list):
        return ext.name, ext.obj.get_conversion_types()

    @staticmethod
    def on_request_conversion_check(ext: Extension, data: float,
                                    from_type: str, to_type: str) -> bool:
        _, types = UnitConversion.get_conversion_types(ext)
        return next(
            (True for t in types if t[0] == from_type and t[1] == to_type),
            False
        )

    @staticmethod
    def on_request_conversion(ext: Extension, data: float, from_type: str,
                              to_type: str) -> (str, float):
        data = ext.obj.on_request_conversion(data, from_type, to_type)
        if data is not None:
            return ext.name, data