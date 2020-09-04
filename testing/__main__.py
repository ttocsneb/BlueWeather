import argparse
import logging
import sys
import unittest

import testing

# Using the option -prog PROG_NAME will change the program name
if "-prog" in sys.argv:
    i = sys.argv.index("-prog")
    prog = sys.argv[i + 1]
    del sys.argv[i:i + 2]
else:
    prog = sys.argv[0]

parser = argparse.ArgumentParser(
    description='BlueWeather TestSuite', prog=prog
)

parser.add_argument(
    '--level', dest='level',
    choices=['DEBUG', 'INFO', 'WARNING',
             'ERROR', 'CRITICAL'],
    help="Set Log Level, default CRITICAL"
)
parser.add_argument(
    '-i', '--info', dest='level', action='store_const',
    const='INFO',
    help="Enable debug logging. equivalent to --level INFO"
)
parser.add_argument(
    '-v', '-d', '--debug', dest='level', action='store_const',
    const='DEBUG',
    help="Enable debug logging. equivalent to --level DEBUG"
)
parser.add_argument(
    '-e', '--error', dest='level', action='store_const',
    const='ERROR',
    help="Enable debug logging. equivalent to --level INFO"
)
parser.add_argument(
    '-f', '--fail-fast', dest="failfast", action="store_true", default=False,
    help="Stop the tests after the first failure."
)

args = parser.parse_args(sys.argv[1:])

logging.getLogger().setLevel(args.level or 'CRITICAL')

runner = unittest.TextTestRunner(failfast=args.failfast, verbosity=2)
runner.run(testing.suite())
