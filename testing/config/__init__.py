import logging
import os
import shutil
import unittest

from ruamel import yaml
from blueweather.config import Config

_logger = logging.getLogger(__name__)
_dir_name = os.path.dirname(__file__)
_conf_file = os.path.join(_dir_name, "config.yml")
_override_conf_file = os.path.join(_dir_name, "test_override.yml")


class ConfigTester(unittest.TestCase):
    """
    Test everything related to blueweather.config
    """

    def setUp(self):
        if os.path.exists(_conf_file):
            os.remove(_conf_file)

    def tearDown(self):
        if os.path.exists(_conf_file):
            os.remove(_conf_file)

    def test_save(self):
        config = Config(_conf_file)
        self.assertFalse(os.path.exists(_conf_file))
        config.save()
        self.assertTrue(os.path.exists(_conf_file))

    def test_creation(self):
        config = Config(_conf_file)
        self.assertFalse(os.path.exists(_conf_file))
        config.load()
        self.assertTrue(os.path.exists(_conf_file))

    def test_default_strip(self):
        config = Config(_conf_file)
        config.save()
        self.assertTrue(os.path.exists(_conf_file))

        with open(_conf_file) as f:
            data = yaml.safe_load(f)

        self.assertIn("secret_key", data)
        self.assertNotIn("debug", data)

    def test_load_data(self):
        shutil.copyfile(_override_conf_file, _conf_file)
        config = Config(_conf_file)
        config.load()

        self.assertEqual(config.debug, False)
        self.assertEqual(config.web.static_url, "/foo/")

    def test_overrides(self):
        shutil.copyfile(_override_conf_file, _conf_file)
        config = Config(_conf_file)
        config.load()
        config.save()

        with open(_conf_file) as f:
            data = yaml.safe_load(f)

        self.assertIn("secret_key", data)
        self.assertIn("debug", data)
        self.assertIn("web", data)
        self.assertIn("static_url", data["web"])

    def test_modified(self):
        shutil.copyfile(_override_conf_file, _conf_file)
        config = Config(_conf_file)
        config.load()
        self.assertTrue(config.modified)
        config.save()
        self.assertFalse(config.modified)
