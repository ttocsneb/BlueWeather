from blueweather.plugins.base import Weather


class DummyWeather(Weather):
    def on_weather_request(self):
        return {}
