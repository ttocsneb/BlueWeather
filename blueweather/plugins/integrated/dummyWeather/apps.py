from django.apps import AppConfig


class DummyWeatherConfig(AppConfig):
    name = 'blueweather.plugins.integrated.dummyWeather'
    label = 'dummyWeather'
    verbose_name = 'Dummy Weather'

    description = """A fake weather plugin for development of other plugins.
    """

    summary = description.splitlines()[0]
