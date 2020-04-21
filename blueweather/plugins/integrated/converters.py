from blueweather.plugins.base import UnitConversion, Plugin


class ImperialConversion(UnitConversion, Plugin):
    def get_plugin_name(self):
        return "Imperial Conversion"

    def get_plugin_description(self):
        return "Provides conversions for common american units."

    def get_conversion_types(self):
        return [
            ('celsius', 'fahrenheit'),
            ('meter', 'feet'),
            ('meter', 'mile'),
            ('meter', 'yard'),
            ('kilogram', 'pound'),
            ('meter/second', 'mile/hour'),
            ('newton', 'pound'),
            ('pascal', 'inch of mercury')
        ]

    def on_request_conversion(self, data, from_type, to_type):
        if from_type == 'celsius' and to_type == 'fahrenheit':
            return (data * 9 / 5) + 32
        if from_type == 'meter':
            if to_type == 'feet':
                return data * 3.28084
            if to_type == 'mile':
                return data * 0.000621371
            if to_type == 'yard':
                return data * 1.09361
        if from_type == 'kilogram' and to_type == 'pound':
            return data * 2.20462
        if from_type == 'meter/second' and to_type == 'mile/hour':
            return data * 2.23694
        if from_type == 'newton' and to_type == 'pound':
            return data * 0.224809
        if from_type == 'pascal' and to_type == 'inch of mercury':
            return data * 0.0002953


class MetricConversion(UnitConversion, Plugin):
    def get_plugin_name(self):
        return "Metric Conversion"

    def get_plugin_description(self):
        return "Provides conversions for common metric units."

    def get_conversion_types(self):
        return [
            ('meter', 'centimeter'),
            ('meter', 'kilometer'),
            ('meter', 'millimeter'),
            ('kilogram', 'gram'),
            ('meter/second', 'kilometer/hour'),
            ('newton', 'kilogram'),
            ('pascal', 'bar'),
            ('pascal', 'kilopascal')
        ]

    def on_request_conversion(self, data, from_type, to_type):
        if from_type == 'meter':
            if to_type == 'centimeter':
                return data * 100
            if to_type == 'millimeter':
                return data * 1000
            if to_type == 'kilometer':
                return data / 1000
        if from_type == 'kilogram' and to_type == 'gram':
            return data * 1000
        if from_type == 'meter/second' and to_type == 'kilometer/hour':
            return data / 3.6
        if from_type == 'newton' and to_type == 'kilogram':
            return data / 9.80665
        if from_type == 'pascal':
            if to_type == 'kilopascal':
                return data / 1000
            if to_type == 'bar':
                return data / 100000
