from blueweather.plugins.base import Startup, Plugin

class DummyStartup(Plugin, Startup):

    def on_startup(self):
        print("hello World! I have started up!")

    def get_plugin_name(self):
        return "Dummy Startup"
    
    def get_plugin_description(self):
        return "A Test plugin for checking if the startup plugins work."
    
    def get_plugin_author(self):
        return "Benjamin Jacobs"
    
    def get_plugin_url(self):
        return "https://github.com/ttocsneb/blueweather"