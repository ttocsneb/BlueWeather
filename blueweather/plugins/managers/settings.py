from stevedore import EnabledExtensionManager
from stevedore.extension import Extension

from blueweather.config import Config

from .. import dao

import logging


class SettingsManager(EnabledExtensionManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings_intialized = False
        self._logger = logging.getLogger(__name__)

    def load_settings(self, config: Config):
        """
        Load the settings for all the plugins
        """
        # Load the settings
        self._logger.info("Loading %d settings plugins", len(self.extensions))

        for ext in self.extensions:
            self._load_one_setting(config, ext)

        if not self._settings_intialized:
            for ext in self.extensions:
                dao.Settings.on_settings_initialized(ext)
            
            self._settings_intialized = True

    def unload_settings(self, config: Config):
        """
        Unload the settings for all the plugins
        """
        self._logger.info("Unloading %d settings plugins", len(self.extensions))
        for ext in self.extensions:
            self._unload_one_setting(config, ext)
    
    def _load_one_setting(self, config: Config, ext: Extension):
        if ext.name not in config.extensions.settings:
            config.extensions.settings[ext.name] = dict()
        
        # Migrate the settings
        settings = config.extensions.settings[ext.name]
        migration, changed = dao.Settings.settings_migrate(ext, settings)
        config.extensions.settings[ext.name] = migration
        if changed:
            config.modified = True

        # Deserialize the settings
        dao.Settings.settings_deserialize(ext, migration)

    def _unload_one_setting(self, config: Config, ext: Extension):
        # Serialize the settings
        settings = config.extensions.settings[ext.name]
        serialized = dao.Settings.settings_serialize(ext, settings)

        # Apply the settings
        config.extensions.settings[ext.name] = serialized
