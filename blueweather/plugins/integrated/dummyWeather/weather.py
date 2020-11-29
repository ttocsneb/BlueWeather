from blueweather.plugins.apps.weather import Weather


class DummyWeather(Weather):
    def on_weather_request(self):
        return {}
