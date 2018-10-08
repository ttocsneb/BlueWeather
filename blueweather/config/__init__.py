"""
Config Package
"""

import os
from ruamel import yaml

from . import web


class Config:
    """
    The Config object contains a yaml configuration file.  You can access its
    contents as a dictionary.
    """

    def __init__(self, file, defaults=None):
        """
        Create a new Config object

        The config file will be loaded immediately after creation

        :param str file: The file of the config

        :param callable or dict defaults: Can be a callable or a dict.  Should
            return the default values for the config
        """
        self._file = file
        self._config = dict()
        self._defaults = defaults

        self.load()

    def save(self):
        """
        Save the Config to file
        """

        stream = open(self._file, 'w')
        res = yaml.round_trip_dump(self._config, indent=2, block_seq_indent=1)

        stream.write(res)
        stream.close()

    def load_defaults(self, save=False):
        """
        Load the default values for the config

        :param bool save: if True, the default values will be saved to file
        """
        if self._defaults:
            if callable(self._defaults):
                self._config = self._defaults()
            else:
                self._config = self._defaults

            if save:
                self.save()

    def load(self):
        """
        Load the config from file

        If the file does not exist, a new default one will be created
        """
        if not os.path.exists(self._file):
            self.load_defaults(True)
            return
        stream = open(self._file, 'r')
        self._config = yaml.round_trip_load(stream)

    def __len__(self):
        return len(self._config)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except:
            return default

    def __contains__(self, value):
        return value in self._config


class WebConfig(Config):
    """
    The BlueWeather's Configuration object.  It implements some explicit
    objects that the configuration must include
    """

    def __init__(self, file):
        super().__init__(file, self._get_defaults)

        self.web = None

        self._load_config()

    def _get_defaults(self):
        self.web = web.WebConfig()

        conf = dict()
        conf['web'] = self.web.getObject()
        return conf

    def _load_config(self):
        self.web = web.WebConfig.loadObject(self._config['web'])

    def _udpate_config(self):
        self._config['web'] = self.web.getObject()

    def save(self):
        self._udpate_config()

        super().save()

    def load(self):
        super().load()

        self._load_config()
