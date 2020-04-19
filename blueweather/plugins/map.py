from marshmallow import Schema
from stevedore.extension import Extension


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
