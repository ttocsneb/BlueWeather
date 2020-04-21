import unittest

from . import config
from .plugins import unitConvert


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(config))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(unitConvert))
    return suite
