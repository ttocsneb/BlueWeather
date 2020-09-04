from blueweather.plugins.base import Weather, Plugin


class DummyWeather(Weather, Plugin):
    def on_weather_request(self):
        return {}

    def get_plugin_name(self):
        return "Dummy Weather"

    def get_plugin_description(self):
        return "This prevents an un-configured setup from crashing."
