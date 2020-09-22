import unittest

from stevedore.extension import Extension

from blueweather.config import objects
from blueweather.plugins import Extensions
from blueweather.plugins import dao


class UnitConversionTester(unittest.TestCase):
    """
    Test integrated unit conversion plugins
    """

    def setUp(self):
        settings = objects.Config(
            extensions=objects.Extensions(
            )
        )
        self.extensions = Extensions(settings, True)

    def tearDown(self):
        self.extensions = None

    def get_extension(self, name: str) -> Extension:
        return next(
            (e for e in self.extensions.unitConversion.extensions
             if e.name == name),
            None
        )

    def convert(self, data, from_t, to_t):
        return dao.UnitConversion.convert(
            self.extensions.unitConversion, data, from_t, to_t
        )[1]

    def test_loaded(self):
        """
        Make sure that ImperialConversion and MetricConversion extensions
        get loaded
        """
        self.assertIsNotNone(self.get_extension('imperialConverter'))
        self.assertIsNotNone(self.get_extension('metricConverter'))

    def test_metric_conversions(self):
        """
        Make sure metric conversions are correct and the extension manager
        processes the request as it is supposed to
        """
        from_value = 2.45
        centi_conv = 100
        kilo_conv = 1 / 1000
        milli_conv = 1000

        try:
            # Test distances
            self.assertAlmostEqual(
                from_value * centi_conv,
                self.convert(from_value, 'meter', 'centimeter'),
                3
            )
            self.assertAlmostEqual(
                from_value * milli_conv,
                self.convert(from_value, 'meter', 'millimeter'),
                3
            )
            self.assertAlmostEqual(
                from_value * kilo_conv,
                self.convert(from_value, 'meter', 'kilometer')
            )

            # Test Mass
            self.assertAlmostEqual(
                from_value * milli_conv,
                self.convert(from_value, 'kilogram', 'gram'),
                3
            )

            # Test Speed
            self.assertAlmostEqual(
                from_value / 3.6,
                self.convert(from_value, 'meter/second', 'kilometer/hour'),
                3
            )

            # Test Force
            self.assertAlmostEqual(
                from_value / 9.80665,
                self.convert(from_value, 'newton', 'kilogram'),
                3
            )

            # Test Pressure
            self.assertAlmostEqual(
                from_value * 0.00001,
                self.convert(from_value, 'pascal', 'bar')
            )
            self.assertAlmostEqual(
                from_value * kilo_conv,
                self.convert(from_value, 'pascal', 'kilopascal'),
                3
            )
        except KeyError as err:
            self.fail(msg="Should not raise exception: %s" % err)

    def test_imperial_conversions(self):
        """
        Test imperial conversions
        """
        from_value = 5.132

        try:
            # Test Temperature
            self.assertAlmostEqual(
                from_value * 9 / 5 + 32,
                self.convert(from_value, 'celsius', 'fahrenheit')
            )

            # Test Distance
            self.assertAlmostEqual(
                from_value * 3.280839,
                self.convert(from_value, 'meter', 'feet'),
                3
            )
            self.assertAlmostEqual(
                from_value * 3.280839 / 5280,
                self.convert(from_value, 'meter', 'mile'),
                3
            )
            self.assertAlmostEqual(
                from_value * 3.280839 / 3,
                self.convert(from_value, 'meter', 'yard'),
                3
            )

            # Test mass/force
            self.assertAlmostEqual(
                from_value * 2.204623,
                self.convert(from_value, 'kilogram', 'pound'),
                3
            )
            self.assertAlmostEqual(
                from_value / 9.80665 * 2.204623,
                self.convert(from_value, 'newton', 'pound'),
                3
            )

            # Test Speed
            self.assertAlmostEqual(
                from_value / 0.44704,
                self.convert(from_value, 'meter/second', 'mile/hour'),
                3
            )

            # Test Pressure
            self.assertAlmostEqual(
                from_value / 3386.39,
                self.convert(from_value, 'pascal', 'inch of mercury'),
                3
            )
        except KeyError as err:
            self.fail(msg="Should not raise exception: %s" % err)

    def test_advanced_conversions(self):
        """
        Test conversions that aren't explicitly defined
        """

        # Test newton to gram
        try:
            self.assertAlmostEqual(
                45.789 / 9.80665 * 1000,
                self.convert(45.789, 'newton', 'gram')
            )
        except KeyError as err:
            self.fail(msg="Should not raise exception: %s" % err)
