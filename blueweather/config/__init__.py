import logging
import os

from ruamel import yaml

from . import objects, schemes

_logger = logging.getLogger(__name__)


class Config(objects.Config):
    def __init__(self, directory: str):
        # Secret_key is populated with an empty string to prevent a new key
        # from being generated everytime config is initialized
        super().__init__(secret_key="", web=objects.Web(api_key=''))
        self._directory = directory

    def __apply(self, obj: objects.Config):
        self.web = obj.web
        self.debug = obj.debug
        self.secret_key = obj.secret_key
        self.time_zone = obj.time_zone
        self.modified = obj.modified
        self.extensions = obj.extensions
        self.commands = obj.commands

    def set_defaults(self):
        self.__apply(objects.Config())

    def load(self):
        """
        Load the config file
        """

        try:
            with open(self._directory) as conf:
                config = yaml.safe_load(conf)
        except FileNotFoundError:
            _logger.warn("Could not find %s! Creating default config..",
                         self._directory)
            self.set_defaults()
            self.save()
            return

        schema = schemes.ConfigSchema()

        self.__apply(schema.load(config))

    def save(self):
        """
        Save the config file
        """

        schema = schemes.ConfigSchema()
        data = schema.dump(self)

        # Merge the original settings with the new settings
        if os.path.isfile(self._directory):
            with open(self._directory) as conf:
                old_data = yaml.safe_load(conf)

            def recursive_merge(orig: dict, new: dict):
                for k, v in new.items():
                    if k in orig:
                        if isinstance(v, dict):
                            orig[k] = recursive_merge(orig[k], v)
                        elif orig[k] != v:
                            orig[k] = v
                    else:
                        orig[k] = v
                return orig

            data = recursive_merge(old_data, data)

        with open(self._directory, 'w') as conf:
            _logger.info("Saving config to %s", self._directory)
            yaml.dump(data, conf)

        self.modified = False
