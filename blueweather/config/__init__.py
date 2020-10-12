import logging
import os

from ruamel import yaml

from . import objects, schemas


class Config(objects.Config):
    def __init__(self, directory: str):
        # Secret_key is populated with an empty string to prevent a new key
        # from being generated everytime config is initialized
        super().__init__(calculate_secret=False)
        self._directory = directory
        self._logger = logging.getLogger(__name__)

    def __apply(self, obj: objects.Config):
        self.web = obj.web
        self.system = obj.system
        self.plugins = obj.plugins
        self.apps = obj.apps
        self.version = obj.version
        self.modified = obj.modified

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
            self._logger.warn(
                "Could not find %s! Creating default config..",
                self._directory)
            self.set_defaults()
            self.save()
            return

        schema = schemas.Config()

        self.__apply(schema.load(config))

    def save(self):
        """
        Save the config file
        """

        schema = schemas.Config()
        data = schema.dump(self)

        with open(self._directory, 'w') as conf:
            self._logger.info("Saving config to %s", self._directory)
            yaml.dump(data, conf)

        self.modified = False

    def serialize(self) -> dict:
        """
        Serialize the settings into a dictionary

        :return: settings
        """
        from . import internal_schemas

        schema = internal_schemas.Config()
        data = schema.dump(self)
        return data

    def deserialize(self, data: dict):
        """
        Deserialize the settings from a dictionary

        :param data: settings
        """
        from . import internal_schemas

        schema = internal_schemas.Config()
        self.__apply(schema.load(data))
