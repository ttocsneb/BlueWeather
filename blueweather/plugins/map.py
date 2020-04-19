from marshmallow import Schema
from stevedore.extension import Extension, ExtensionManager


def strip_name(tup: tuple):
    return map(lambda x: x[1], tup)


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
    def get_app_name(ext: Extension) -> (str, str):
        return ext.name, ext.obj.get_app_name()

    @staticmethod
    def get_url_info(ext: Extension) -> (str, str, str):
        data = ext.obj.get_url_info()
        if isinstance(data, tuple):
            return ext.name, data[0], data[1]
        return ext.name, data, data.replace('/', '.')


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
    def conversions(man: ExtensionManager) -> dict:
        units = dict()
        for _, conversions in man.map(UnitConversion.get_conversion_types):
            for from_type, to_type in conversions:
                if from_type not in units:
                    units[from_type] = set()
                units[from_type].add(to_type)

    @staticmethod
    def all_conversions(man: ExtensionManager = None, units: dict = None
                        ) -> dict:
        if units is None:
            units = UnitConversion.conversions(man)
        # Add secondary conversions (Conversions that can be made by
        # converting a conversion)
        for k, v in units.items():
            for u in v:
                if u in units:
                    v.union(units[u])

    @staticmethod
    def convert(man: ExtensionManager, data: float, from_type: str,
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
        for k, v in units:
            if v == to_type:
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
        return ext.obj.get_conversion_types()

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
