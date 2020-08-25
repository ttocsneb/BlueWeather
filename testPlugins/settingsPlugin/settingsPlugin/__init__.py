from blueweather.plugins.base import Plugin, Settings

from marshmallow import fields, Schema, post_load


class SettingsObject:
    def __init__(self, description: str):
        self.description = description

    def __repr__(self):
        return "SettingsObject<description='{}'>".format(self.description)


class SettingsSchema(Schema):
    description = fields.String()

    @post_load
    def loadSettings(self, data, **kwargs):
        return SettingsObject(**data)


class DummySettings(Plugin, Settings):

    def get_plugin_name(self):
        return "Dummy Settings"

    def get_plugin_description(self):
        return "A Dummy Plugin used for testing that settings actually work."

    def get_plugin_author(self):
        return "Benjamin Jacobs"

    def get_plugin_url(self):
        return "https://github.com/ttocsneb/blueweather"

    def on_settings_initialized(self):
        print("the settings have been initialized!")
        print("the settings object is: %s" % self._settings)

    def settings_deserialize(self, data: dict):
        schema = SettingsSchema()
        return schema.load(data)
    
    def settings_serialize(self, data: Settings):
        schema = SettingsSchema()
        return schema.dump(data)
    
    def settings_migrate(self, version: int, settings: dict):
        modified = False
        if version == 0:
            settings['description'] = "Hello World!"
            modified = True
            print("Migration 0->1")
        return 1, settings, modified