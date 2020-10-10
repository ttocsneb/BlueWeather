from blueweather.plugins.base import UnitConversion


class ImperialConversion(UnitConversion):
    def get_conversion_types(self):
        return [
            ('c', 'f'),
            ('m', 'ft'),
            ('m', 'mi'),
            ('m', 'yd'),
            ('kg', 'lb'),
            ('m/s', 'mph'),
            ('N', 'lbf'),
            ('Pa', 'inHg'),
            ('Pa', 'psi')
        ]

    def conversion_request(self, data, from_type, to_type):
        if from_type == 'c' and to_type == 'f':
            return (data * 9 / 5) + 32
        if from_type == 'm':
            if to_type == 'ft':
                return data * 3.28084
            if to_type == 'mi':
                return data * 0.000621371
            if to_type == 'yd':
                return data * 1.09361
        if from_type == 'kg' and to_type == 'lb':
            return data * 2.20462
        if from_type == 'm/s' and to_type == 'mph':
            return data * 2.23694
        if from_type == 'N' and to_type == 'lbf':
            return data * 0.224809
        if from_type == 'Pa' and to_type == 'inHg':
            return data * 0.0002953
        if from_type == 'Pa' and to_type == 'psi':
            return data / 6894.75729


class MetricConversion(UnitConversion):
    def get_conversion_types(self):
        return [
            ('m', 'cm'),
            ('m', 'km'),
            ('m', 'mm'),
            ('kg', 'g'),
            ('m/s', 'km/h'),
            ('N', 'kgf'),
            ('Pa', 'bar'),
            ('Pa', 'kPa')
        ]

    def conversion_request(self, data, from_type, to_type):
        if from_type == 'm':
            if to_type == 'cm':
                return data * 100
            if to_type == 'mm':
                return data * 1000
            if to_type == 'km':
                return data / 1000
        if from_type == 'kg' and to_type == 'g':
            return data * 1000
        if from_type == 'm/s' and to_type == 'km/h':
            return data / 3.6
        if from_type == 'N' and to_type == 'kgf':
            return data / 9.80665
        if from_type == 'Pa':
            if to_type == 'kPa':
                return data / 1000
            if to_type == 'bar':
                return data / 100000
